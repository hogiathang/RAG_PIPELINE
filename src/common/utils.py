import ast
import json
import re
from typing import Any


def _strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _remove_js_comments(text: str) -> str:
    no_block_comments = re.sub(r"/\*[\s\S]*?\*/", "", text)
    return re.sub(r"(^|\s)//.*$", "", no_block_comments, flags=re.MULTILINE)


def _remove_trailing_commas(text: str) -> str:
    # Make near-JSON payloads valid when the model leaves trailing commas.
    return re.sub(r",\s*([}\]])", r"\1", text)


def _extract_json_candidates(text: str) -> list[str]:
    candidates = []
    stack = []
    start_idx = None

    for idx, ch in enumerate(text):
        if ch in "[{":
            if not stack:
                start_idx = idx
            stack.append(ch)
        elif ch in "]}":
            if not stack:
                continue

            opener = stack[-1]
            if (opener == "{" and ch == "}") or (opener == "[" and ch == "]"):
                stack.pop()
            else:
                # Reset on malformed nesting and continue scanning.
                stack.clear()
                start_idx = None
                continue

            if not stack and start_idx is not None:
                candidates.append(text[start_idx : idx + 1])
                start_idx = None

    # Prefer larger spans first to capture the full object before nested ones.
    candidates.sort(key=len, reverse=True)
    return candidates


def _try_json_load(text: str) -> Any:
    return json.loads(text, strict=False)


def _try_python_literal(text: str) -> Any:
    parsed = ast.literal_eval(text)
    if isinstance(parsed, (dict, list)):
        return parsed
    raise ValueError("Parsed literal is not a dict or list.")


def format_json_response(response: str) -> Any:
    if response is None:
        raise ValueError("Response is None; cannot parse JSON.")

    if isinstance(response, (dict, list)):
        return response

    if not isinstance(response, str):
        raise TypeError(f"Unsupported response type: {type(response)}")

    cleaned = _strip_code_fences(response)

    # 1) Fast path: direct strict/near-strict JSON.
    try:
        return _try_json_load(cleaned)
    except Exception:
        pass

    # 2) Near-JSON path: remove JS comments/trailing commas and retry.
    normalized = _remove_trailing_commas(_remove_js_comments(cleaned)).strip()
    try:
        return _try_json_load(normalized)
    except Exception:
        pass

    # 3) Extract balanced JSON-like candidates from surrounding text.
    for candidate in _extract_json_candidates(normalized):
        try:
            return _try_json_load(candidate)
        except Exception:
            try:
                return _try_python_literal(candidate)
            except Exception:
                continue

    # 4) Final fallback: Python literal payload (single quotes/None/True/False).
    try:
        return _try_python_literal(normalized)
    except Exception as exc:
        preview = normalized[:240].replace("\n", "\\n")
        raise ValueError(
            f"No valid JSON object found in response. Preview: {preview}"
        ) from exc
