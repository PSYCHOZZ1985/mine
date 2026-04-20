import json
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "settings.example.json"


def load_settings(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)

    try:
        with config_path.open("r", encoding="utf-8") as file:
            settings = json.load(file)
    except FileNotFoundError as error:
        raise ValueError(f"Config file not found: {config_path}") from error
    except json.JSONDecodeError as error:
        message = (
            f"Config file is not valid JSON: {config_path} "
            f"(line {error.lineno}, column {error.colno})"
        )
        raise ValueError(message) from error

    if not isinstance(settings, dict):
        raise ValueError(f"Config file must contain a JSON object: {config_path}")

    return settings


def build_message(settings: dict[str, Any]) -> str:
    app_name = str(settings.get("app_name", "application"))
    log_level = str(settings.get("log_level", "INFO")).upper()
    debug_status = "enabled" if settings.get("debug", False) else "disabled"

    return f"{app_name} is ready. Log level: {log_level}. Debug mode: {debug_status}."


def main(config_path: str | Path = DEFAULT_CONFIG_PATH) -> int:
    try:
        settings = load_settings(config_path)
    except ValueError as error:
        print(f"Configuration error: {error}")
        return 1

    print(build_message(settings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
