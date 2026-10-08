from pathlib import Path
import tomllib
import unittest


class MetadataTests(unittest.TestCase):
    def test_readme_exists(self):
        root = Path(__file__).resolve().parents[1]
        with (root / "pyproject.toml").open("rb") as stream:
            metadata = tomllib.load(stream)
        self.assertTrue((root / metadata["project"]["readme"]).is_file())
