"""Setup and initialization for Unit Tests."""

import os
import pytest
import yaml


test_dir = os.path.dirname(os.path.realpath(__file__)) + '/.unittest'
if not os.path.exists(test_dir):
    os.mkdir(test_dir)


def remove_file_if_existed(file_path):
    """Remove one file if it is existed!"""

    if os.path.isfile(file_path):
        return os.remove(file_path)


@pytest.fixture
def fix_test_conf_setup_yml():
    """Remove existed yml file and create a new ones."""

    yml_content = {
        'key1': 'value1'
    }

    sample_yml_path = test_dir + '/sample.yml'
    remove_file_if_existed(sample_yml_path)
    sample_yml_file = open(sample_yml_path, 'w')

    yaml.dump(yml_content, sample_yml_file)
    sample_yml_file.close()

    return sample_yml_path


@pytest.fixture
def fix_test_conf_reset():
    """Reset the Config instance to None for testing."""
    
    from corecat.config import Config

    Config.instance = None
