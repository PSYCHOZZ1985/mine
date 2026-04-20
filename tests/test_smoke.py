import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.main import build_message, load_settings


class TestSettings(unittest.TestCase):
    def test_load_settings_reads_valid_config(self) -> None:
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "settings.json"
            config_path.write_text(
                '{"app_name": "demo", "debug": false, "log_level": "warning"}',
                encoding="utf-8",
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

    def test_load_settings_rejects_invalid_json(self) -> None:
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "settings.json"
            config_path.write_text("{broken json", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "not valid JSON"):
                load_settings(config_path)


if __name__ == "__main__":
    unittest.main()
