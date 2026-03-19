from pathlib import Path
import logging


class AppLogger:
    """Centralized logger manager for console and file logging."""

    _configured = False
    _default_logger_name = "rag_pipeline"

    @classmethod
    def setup(
        cls,
        level: int = logging.INFO,
        log_filename: str = "rag_pipeline.log",
    ) -> logging.Logger:
        if cls._configured:
            return logging.getLogger(cls._default_logger_name)

        project_root = Path(__file__).resolve().parents[2]
        report_dir = project_root / "report"
        report_dir.mkdir(parents=True, exist_ok=True)
        log_file = report_dir / log_filename

        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        if not root_logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        cls._configured = True
        root_logger.info("Logger initialized. Writing logs to %s", log_file)
        return logging.getLogger(cls._default_logger_name)

    @classmethod
    def get_logger(cls, name: str | None = None) -> logging.Logger:
        if not cls._configured:
            cls.setup()
        return logging.getLogger(name or cls._default_logger_name)
