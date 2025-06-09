from pathlib import Path
import json


def test_vault_dir_exists():
    assert Path("vault").exists()


def test_can_write_sample(tmp_path):
    p = tmp_path / "demo.json"
    obj = {"meta": {"id": 1}, "content": "print('hi')"}
    p.write_text(json.dumps(obj))
    loaded = json.loads(p.read_text())
    assert loaded["meta"]["id"] == 1

