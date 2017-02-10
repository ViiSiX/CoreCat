"""Setup and initialization for Unit Tests."""

import os
import pytest
import yaml
from corecat.config import Config


test_dir = os.path.dirname(os.path.realpath(__file__)) + '/.unittest'
if not os.path.exists(test_dir):
    os.mkdir(test_dir)


def remove_file_if_existed(file_path):
    """Remove one file if it is existed!"""
    if os.path.isfile(file_path):
        return os.remove(file_path)


@pytest.fixture
def fix_test_conf_setup_yaml():
    yaml_content = {
        'key1': 'value1'
    }

    sample_yaml_path = test_dir + '/sample.yaml'
    remove_file_if_existed(sample_yaml_path)
    sample_yaml_file = open(sample_yaml_path, 'w')

    yaml.dump(yaml_content, sample_yaml_file)
    sample_yaml_file.close()

    return sample_yaml_path
