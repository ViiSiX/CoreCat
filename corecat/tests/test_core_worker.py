import pytest
from corecat.worker import Worker
from corecat.config import ConfigNotLoadedException


class TestCoreWorker(object):
    """Unit tests for corecat.worker.Worker class."""

    def test_should_be_loaded_before_init(self, fix_test_conf_reset):
        with pytest.raises(ConfigNotLoadedException):
            w1 = Worker(0)
