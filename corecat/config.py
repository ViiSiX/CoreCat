"""
In this module, defined the DanceCat config class
which will be used to read configurations from YAML
file. In that file we have:

- Modules' configurations.
- DanceCat's configuration parameters.
"""

import yaml
from os import path, environ


class Config(object):
    """
    This is a Singleton class which will be consisted through all
    the application. One single instance will be created when DanceCat
    is started up, upon that, every time the class being re-created,
    returned pre-loaded values from __Config instance.
    """

    DANCECAT_CONFIGFILE_VAR_NAME = 'DANCECAT_CONFIG_FILE'

    class __Config(object):
        """Subclass of Config which is logically, private."""

        def __init__(self):
            """__Config class initialize."""

            self.params = None
            self.is_loaded = False

            # Check if there is configuration file path in environment vars.
            self.load_from_env_var()

        def __getitem__(self, item):
            """Make the class return values in config['param_name'] format."""
            if self.params is None:
                raise TypeError('Config should be load from file first!')
            return self.params[item]

        def load(self, file_path):
            """Reading values from YAML file and storing the values.
            Configuration file should be encoded in utf-8.

            :param file_path: Path to configuration file in YAML format.
            :type file_path: str
            """

            if not file_path.endswith('.yaml'):
                raise ValueError('The file {0} is not YAML file!'.format(
                    file_path
                ))

            if not path.isfile(file_path):
                raise IOError('The file {0} is not existed!'.format(
                    file_path
                ))

            try:
                self.params = yaml.load(open(file_path, 'r', encoding="utf-8"))
            except TypeError:
                self.params = yaml.load(open(file_path, 'r'))
            self.is_loaded = True

        def load_from_env_var(self):
            """If there is configuration file path in environment variables,
            load configuration from it.
            """
            file_name = environ.get(Config.DANCECAT_CONFIGFILE_VAR_NAME)
            if file_name is not None:
                self.load(file_name)

    # Set up instance.
    instance = None

    def __new__(cls, *args, **kwargs):
        if not Config.instance:
            Config.instance = Config.__Config()

        return Config.instance


class ConfigNotLoadedException(Exception):
    """When configs not loaded yet, raise this exception."""

    def __init__(self):

        # Calling the base lass constructor.
        super(ConfigNotLoadedException, self).__init__(
            'Configs must be loaded before using.'
        )
