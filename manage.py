from app import create_app
from support.config import Config
from support.file_config import FileConfig
from support.logging_configurator import LoggingConfigurator


def run_app():
    LoggingConfigurator.configure_logging()
    app_config = FileConfig()
    app = create_app()
    app.run(host=app_config.get_value(Config.APP_CONFIG, Config.SERVER_HOST),
            port=int(app_config.get_value(Config.APP_CONFIG, Config.SERVER_PORT)))


if __name__ == '__main__':
    run_app()
