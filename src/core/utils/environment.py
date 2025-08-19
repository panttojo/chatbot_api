from enum import StrEnum
from pathlib import Path

from loguru import logger

BASEDIR = Path(__file__).resolve().parents[3]


class EnvironmentEnum(StrEnum):
    """
    Enum that defines the allowed environments in the application.

    Attributes
    ----------
        LOCAL: Local development environment
        DEVELOPMENT: Development environment
        PRODUCTION: Production environment
        TESTING: Testing environment
    """

    LOCAL = "local"
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

    @classmethod
    def get_env_prefix(cls, environment: str) -> str:
        suffixes = {
            cls.LOCAL: "local",
            cls.DEVELOPMENT: "dev",
            cls.PRODUCTION: "prd",
            cls.TESTING: "test",
        }

        suffix = suffixes.get(environment)
        if not suffix:
            error_msg = f"No suffix found for environment '{environment}' in {suffixes}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        return suffix

    @classmethod
    def get_env_file(cls, environment: str) -> Path:
        """
        Get the path of the .env file corresponding to the specified environment.

        Args:
            environment: The environment for which to get the .env file

        Returns
        -------
            Path: The path to the corresponding .env file

        Raises
        ------
            ValueError: If the environment is not valid or has no corresponding suffix
        """
        logger.info(f"Getting env file for environment: {environment}")

        suffix = cls.get_env_prefix(environment)
        env_file_name = f"envs/.env.{suffix}"
        return Path.joinpath(BASEDIR, env_file_name)
