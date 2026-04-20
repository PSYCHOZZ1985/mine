import unittest

from src.main import main


class TestSmoke(unittest.TestCase):
    def test_main_exists(self) -> None:
        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()
