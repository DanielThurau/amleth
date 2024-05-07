from dotenv import load_dotenv
import os
from pathlib import Path


class Config:
    """
    Base class for configuration management.
    """

    def __init__(self):
        self.config = {}

    def load(self):
        """
        Load the configuration into the config dictionary.
        This method should be overridden by subclasses to implement specific loading logic.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get(self, key, default=None):
        """
        Retrieve a value from the configuration.
        """
        return self.config.get(key, default)


class EnvConfig(Config):
    """
    Configuration class that loads from a .env_prod file.
    """

    def __init__(self, env_file=None):
        super().__init__()
        self.env_file = env_file or ".env"
        self.load()

    def load(self):
        """
        Load the configuration from a .env_prod file.
        """
        env_path = Path(".") / self.env_file
        load_dotenv(dotenv_path=env_path)
        self.config = {key: os.getenv(key) for key in os.environ}
