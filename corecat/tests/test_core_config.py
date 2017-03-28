import pytest
from corecat.config import Config


class TestCoreConfig(object):
    """Unit tests for corecat.config.Config class."""

    def test_should_be_singleton(self):
        """Config should be a singleton class."""

        c0 = Config()
        c1 = Config()

        assert c0 == c1

    def test_config_should_have_loaded(self):
        """Config should be loaded in previous tests."""

        c0 = Config()
        with pytest.raises(TypeError):
            c0['config_key']

    def test_config_would_be_loaded(self, fix_test_conf_setup_yaml):
        """Config should consist in every initiated class. It's also able to
        load values after initiation."""

        c0 = Config()
        assert not c0.is_loaded

        c0.load(fix_test_conf_setup_yaml)
        assert c0.is_loaded
        assert c0['key1'] == 'value1'

        c1 = Config()
        assert c1['key1'] == 'value1'

    def test_config_would_be_loaded_from_env_var(self,
                                                 monkeypatch,
                                                 fix_test_conf_reset,
                                                 fix_test_conf_setup_yaml):
        """Config can also auto-load from environment variables."""

        monkeypatch.setenv(Config.DANCECAT_CONFIGFILE_VAR_NAME,
                           fix_test_conf_setup_yaml)
        c0 = Config()
        assert c0.is_loaded
        assert c0['key1'] == 'value1'

    def test_config_would_load_failed(self):
        """Config can not be loaded if the given file is in other format or
        does not exist."""

        c0 = Config()
        with pytest.raises(ValueError):
            c0.load('/path/to/some/where')

        with pytest.raises(IOError):
            c0.load('/path/to/some/where.yml')
