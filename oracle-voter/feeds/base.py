from common import client
import os
import errno
from os.path import abspath, expanduser
import plyvel


class Base:

    def __init__(self, api_url):
        self.api_url = api_url
        self.client = client
        self.name = "XXX"  # Name of the exchange
        self.base_dir = expanduser(
            os.environ.get("ORACLE_VOTER_HOME", "~/.oracle-voter")
        )
        # EAFP
        try:
            os.makedirs(abspath(self.base_dir))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        db_path = f"{abspath(self.base_dir)}/{self.name}.ldb"
        print(db_path)
        self.db = plyvel.DB(db_path, create_if_missing=True)

    def graceful_exit(self):
        self.db.close()
