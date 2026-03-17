import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from src.common.model.agent_adapter import AgentAdapter
from src.common.model.gemini_agent import GeminiAgent
from src.common.model.local_agent import LocalAgent


def _extract_json_object(response: str) -> dict[str, Any]:
    clean_response = (response or "").strip()
    cleaned = re.sub(r"^```json|^```|```$", "", clean_response, flags=re.IGNORECASE).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if not match:
        raise ValueError("No valid JSON object found in the response.")

    return json.loads(match.group(0))


def _safe_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def _normalize_pass1_schema(payload: dict[str, Any], file_name: str) -> dict[str, Any]:
    source_repository = payload.get("source_repository")
    if source_repository in ("", "null"):
        source_repository = None

    search_queries = payload.get("search_queries")
    if not isinstance(search_queries, list):
        search_queries = []
    search_queries = [str(q).strip() for q in search_queries if str(q).strip()]

    raw_skills_details = payload.get("skills_details")
    if not isinstance(raw_skills_details, list):
        raw_skills_details = []

    skills_details: list[dict[str, str]] = []
    for item in raw_skills_details:
        if not isinstance(item, dict):
            continue
        env = str(item.get("execution_environment", "Unknown")).strip()
        if env not in {"Local", "Online", "Unknown"}:
            env = "Unknown"
        skills_details.append(
            {
                "skill_name": str(item.get("skill_name", "Unknown Skill")).strip() or "Unknown Skill",
                "execution_environment": env,
                "justification": str(item.get("justification", "No justification provided.")).strip()
                or "No justification provided.",
            }
        )

    raw_flow = payload.get("skills_flow") if isinstance(payload.get("skills_flow"), dict) else {}
    relationships = raw_flow.get("relationships") if isinstance(raw_flow.get("relationships"), list) else []

    normalized_relationships: list[dict[str, dict[str, Any]]] = []
    for rel in relationships:
        if not isinstance(rel, dict):
            continue
        source = rel.get("source") if isinstance(rel.get("source"), dict) else {}
        sink = rel.get("sink") if isinstance(rel.get("sink"), dict) else {}

        normalized_relationships.append(
            {
                "source": {
                    "code": str(source.get("code", "Unknown Source")).strip() or "Unknown Source",
                    "file": str(source.get("file", file_name)).strip() or file_name,
                    "line_number": _safe_int(source.get("line_number")),
                },
                "sink": {
                    "code": str(sink.get("code", "Unknown Sink")).strip() or "Unknown Sink",
                    "file": str(sink.get("file", file_name)).strip() or file_name,
                    "line_number": _safe_int(sink.get("line_number")),
                },
            }
        )

    return {
        "source_repository": source_repository,
        "search_queries": search_queries,
        "skills_details": skills_details,
        "skills_flow": {
            "description": str(raw_flow.get("description", "No flow description provided.")).strip()
            or "No flow description provided.",
            "relationships": normalized_relationships,
        },
    }


def _build_directory_tree(root_dir: str) -> str:
    root = Path(root_dir)
    lines: list[str] = [f"{root.name}/"]

    def walk(path: Path, prefix: str = "") -> None:
        entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        for idx, entry in enumerate(entries):
            connector = "└── " if idx == len(entries) - 1 else "├── "
            label = entry.name + ("/" if entry.is_dir() else "")
            lines.append(f"{prefix}{connector}{label}")
            if entry.is_dir():
                extension = "    " if idx == len(entries) - 1 else "│   "
                walk(entry, prefix + extension)

    walk(root)
    return "\n".join(lines)


def _build_map_prompt(file_path: str, file_content: str, directory_tree: str) -> str:
    return (
        "Directory Tree:\n"
        f"{directory_tree}\n\n"
        "Analyze exactly one file below while using the tree as global context.\n"
        f"file: {file_path}\n\n"
        "content:\n"
        f"{file_content}"
    )


def _create_agent(use_local_agent: bool = False) -> AgentAdapter:
    if use_local_agent:
        return LocalAgent()
    return GeminiAgent()


def _run_pass1_for_file(agent: AgentAdapter, file_path: str, file_content: str, directory_tree: str) -> dict[str, Any]:
    prompt = _build_map_prompt(file_path=file_path, file_content=file_content, directory_tree=directory_tree)
    response = agent.execute_task(prompt, "agent-extractor")

    raw_json = _extract_json_object(response or "{}")
    normalized = _normalize_pass1_schema(raw_json, file_name=file_path)
    normalized["file"] = file_path
    return normalized


def _run_pass2_global_reasoning(agent: AgentAdapter, package_path: str, directory_tree: str, pass1_results: list[dict[str, Any]]) -> dict[str, Any]:
    aggregated_local_json = json.dumps(pass1_results, ensure_ascii=False, indent=2)
    reduce_prompt = (
        f"Package: {package_path}\n\n"
        "Directory Tree:\n"
        f"{directory_tree}\n\n"
        "Aggregated Local JSON Results (Pass 1):\n"
        f"{aggregated_local_json}\n"
    )

    response = agent.execute_task(reduce_prompt, "global-reasoning")
    try:
        return _extract_json_object(response or "{}")
    except Exception as error:
        print(f"[ERROR] Pass 2 global reasoning failed for '{package_path}': {error}")
        return {
            "global_skills_flow": {
                "description": "Pass 2 global reasoning failed.",
                "relationships": [],
            },
            "cross_file_risks": [],
        }


def run_map_reduce_extraction(
    package_path: str,
    files_data: list[dict[str, str]],
    use_local_agent: bool = False,
    max_workers: int = 8,
) -> dict[str, Any]:
    directory_tree = _build_directory_tree(package_path)
    agent = _create_agent(use_local_agent=use_local_agent)

    if use_local_agent:
        max_workers = 1

    pass1_results: list[dict[str, Any]] = []

    with ThreadPoolExecutor(max_workers=min(max_workers, max(1, len(files_data)))) as executor:
        future_to_file = {
            executor.submit(
                _run_pass1_for_file,
                agent,
                item["file_path"],
                item["content"],
                directory_tree,
            ): item["file_path"]
            for item in files_data
        }

        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                pass1_results.append(future.result())
            except Exception as error:
                print(f"[ERROR] Pass 1 failed for '{file_path}': {error}")
                pass1_results.append(
                    {
                        "file": file_path,
                        "source_repository": None,
                        "search_queries": [],
                        "skills_details": [],
                        "skills_flow": {
                            "description": "Pass 1 extraction failed.",
                            "relationships": [],
                        },
                    }
                )

    pass1_results.sort(key=lambda item: item.get("file", ""))

    cross_file_flow = _run_pass2_global_reasoning(
        agent=agent,
        package_path=package_path,
        directory_tree=directory_tree,
        pass1_results=pass1_results,
    )

    return {
        "package": os.path.basename(package_path.rstrip(os.sep)),
        "directory_tree": directory_tree,
        "pass_1_local_results": pass1_results,
        "pass_2_cross_file_flow": cross_file_flow,
    }