from app.config import Config, FileConfig

def test_empty_config():
    cfg = app.Config()
    pytest.raises(KeyError, cfg.section, 'notexist')
    cfg.add_section('my', {'a': 'b'})
    assert cfg.section('my')['a'] == 'b'


def test_nonexistent():
    pytest.raises(ValueError, FileConfig, 'nonexistent.yml')


def test_default_configs():
    _config = Config()
    _config.configurators.append(FileConfig())

