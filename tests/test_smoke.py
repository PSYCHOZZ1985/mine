import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from src.main import build_message, generate_report, load_settings, main


class TestSettings(unittest.TestCase):
    def write_config(self, content: str) -> Path:
        temp_dir = TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(temp_dir.cleanup)

        config_path = Path(temp_dir.name) / "settings.json"
        config_path.write_text(content, encoding="utf-8")
        return config_path

    def test_load_settings_reads_valid_config(self) -> None:
        config_path = self.write_config(
            '{"app_name": "demo", "debug": false, "log_level": "warning"}',
        )

        settings = load_settings(config_path)

        self.assertEqual(settings["app_name"], "demo")
        self.assertFalse(settings["debug"])
        self.assertEqual(settings["log_level"], "warning")

    def test_build_message_uses_settings(self) -> None:
        settings = {
            "app_name": "demo",
            "debug": True,
            "log_level": "debug",
        }

        message = build_message(settings)

        self.assertEqual(
            message,
            "demo is ready. Log level: DEBUG. Debug mode: enabled.",
        )

    def test_generate_report_uses_settings(self) -> None:
        settings = {
            "app_name": "demo",
            "debug": False,
            "log_level": "warning",
        }

        report = generate_report(settings)

        self.assertIn("Configuration report", report)
        self.assertIn("Application: demo", report)
        self.assertIn("Debug: disabled", report)
        self.assertIn("Log level: WARNING", report)
        self.assertIn("Configuration status: valid", report)

    def test_load_settings_rejects_invalid_json(self) -> None:
        config_path = self.write_config("{broken json")

        with self.assertRaisesRegex(ValueError, "not valid JSON"):
            load_settings(config_path)

    def test_load_settings_rejects_missing_required_field(self) -> None:
        config_path = self.write_config('{"app_name": "demo", "debug": true}')

        with self.assertRaisesRegex(ValueError, "Missing required config field"):
            load_settings(config_path)

    def test_validate_config_cli_reports_success(self) -> None:
        config_path = self.write_config(
            '{"app_name": "demo", "debug": true, "log_level": "info"}',
        )
        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(["--config", str(config_path), "--validate-config"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Config is valid", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_show_config_cli_prints_loaded_config(self) -> None:
        config_path = self.write_config(
            '{"app_name": "demo", "debug": false, "log_level": "warning"}',
        )
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            exit_code = main(["--config", str(config_path), "--show-config"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            json.loads(stdout.getvalue()),
            {"app_name": "demo", "debug": False, "log_level": "warning"},
        )

    def test_output_cli_saves_report_to_file(self) -> None:
        config_path = self.write_config(
            '{"app_name": "demo", "debug": false, "log_level": "warning"}',
        )
        output_path = config_path.parent / "report.txt"
        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(
                ["--config", str(config_path), "--output", str(output_path)],
            )

        self.assertEqual(exit_code, 0)
        self.assertIn("Report saved", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")
        self.assertIn("Application: demo", output_path.read_text(encoding="utf-8"))

    def test_output_cli_reports_invalid_output_path(self) -> None:
        config_path = self.write_config(
            '{"app_name": "demo", "debug": true, "log_level": "info"}',
        )
        output_path = config_path.parent
        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(
                ["--config", str(config_path), "--output", str(output_path)],
            )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("Output error", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
