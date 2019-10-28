import os

from support.config import Config
from support.file_config import FileConfig


class TestFileConfig:

    def test_app_config(self):
        try:
            os.environ['SERVER_PORT'] = '9091'
            app_config = FileConfig()
            server_port = app_config.get_value(Config.APP_CONFIG, Config.SERVER_PORT)
            assert server_port == "9091"
        finally:
            try:
                del os.environ['SERVER_PORT']
            except:
                pass
