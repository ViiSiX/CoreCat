"""Worker is the back-bone class of the DanceCats application. One running
project on DanceCats will run on a worker. It's a sequentially progress running
through functions and plug-ins registered on its hooks. Basic ordered progress:
 - Config loading
 - User loading
 - Metadata loading
 - Data fetching [hooks for data fetching]
 - Data processing [hooks for data processing]
 - Data storing [hooks for data storing]
"""

from corecat.config import Config, \
    ConfigNotLoadedException


class Worker(object):
    """The worker class which will carry all the tasks given to it. When
    finish, the worker will store the results and call the next worker if
    exist.
    """

    def __init__(self, user_id):
        self.config = Config()
        if not self.config.is_loaded:
            raise ConfigNotLoadedException

        self.user_id = user_id
