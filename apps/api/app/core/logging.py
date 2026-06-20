import logging.config

from pythonjsonlogger import jsonlogger

from app.core.config import Settings


class JsonFormatter(jsonlogger.JsonFormatter):
    """Structured JSON formatter with consistent default fields."""

    def add_fields(self, log_record, record, message_dict):  # type: ignore[no-untyped-def]
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault("level", record.levelname)
        log_record.setdefault("logger", record.name)


def configure_logging(settings: Settings) -> None:
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                    "format": "%(asctime)s %(level)s %(name)s %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                }
            },
            "root": {
                "handlers": ["default"],
                "level": settings.log_level,
            },
        }
    )
