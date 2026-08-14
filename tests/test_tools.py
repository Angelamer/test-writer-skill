import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).parents[1]


def load_script(name):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestInvokeModel(unittest.TestCase):
    def test_post_json_sends_bearer_token_without_exposing_it_in_payload(self):
        module = load_script("invoke_model.py")
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b'{"ok": true}'
        with mock.patch.object(module, "urlopen", return_value=response) as urlopen:
            self.assertEqual(
                module.post_json("http://local", {"a": 1}, "secret"), {"ok": True}
            )
        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer secret")
        self.assertNotIn(b"secret", request.data)


class TestReportTool(unittest.TestCase):
    def test_digest_changes_with_file_content(self):
        module = load_script("test_report.py")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.py"
            path.write_text("first", encoding="utf-8")
            first = module.digest(path)
            path.write_text("second", encoding="utf-8")
            self.assertNotEqual(first, module.digest(path))


if __name__ == "__main__":
    unittest.main()
