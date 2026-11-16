import pytest

from project_template.config import load_config


def test_base_merge_and_overrides(tmp_path):
    (tmp_path / "base.toml").write_text('a = 1\ntag = "x"\n[opt]\nlr = 0.1\nname = "adam"\n')
    (tmp_path / "run.toml").write_text('base = "base.toml"\n[opt]\nlr = 0.01\n')
    cfg = load_config(tmp_path / "run.toml", ["opt.lr=3e-4", "tag=fast", "a=[1, 2]"])
    assert cfg == {"a": [1, 2], "opt": {"lr": 3e-4, "name": "adam"}, "tag": "fast"}


@pytest.mark.parametrize("bad", ["step=3", "opt.lrr=1", "a.b=1"])
def test_unknown_override_key_fails(tmp_path, bad):
    (tmp_path / "c.toml").write_text("a = 1\n[opt]\nlr = 0.1\n")
    with pytest.raises(KeyError):
        load_config(tmp_path / "c.toml", [bad])
