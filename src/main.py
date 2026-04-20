import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "settings.example.json"
REQUIRED_FIELDS = ("app_name", "debug", "log_level")


def validate_settings(settings: dict[str, Any], path: str | Path | None = None) -> None:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in settings]

    if missing_fields:
        location = f" in {Path(path)}" if path is not None else ""
        fields = ", ".join(missing_fields)
        raise ValueError(f"Missing required config field(s){location}: {fields}")


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

    validate_settings(settings, config_path)

    return settings


def build_message(settings: dict[str, Any]) -> str:
    app_name = str(settings["app_name"])
    log_level = str(settings["log_level"]).upper()
    debug_status = "enabled" if settings["debug"] else "disabled"

    return f"{app_name} is ready. Log level: {log_level}. Debug mode: {debug_status}."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Load JSON settings and print application status.",
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        type=Path,
        help="Path to a JSON config file.",
    )
    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="Validate the config and print the result.",
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Print the loaded config in a readable format.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        settings = load_settings(args.config)
    except ValueError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 1

    if args.validate_config:
        print(f"Config is valid: {args.config}")
        return 0

    if args.show_config:
        print(json.dumps(settings, indent=2, ensure_ascii=False))
        return 0

    print(build_message(settings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
