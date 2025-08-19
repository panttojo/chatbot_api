import sys
from typing import ClassVar

import sentry_sdk
from loguru import logger
from sentry_sdk.integrations.fastapi import FastApiIntegration

from .base import ENVIRONMENT, EnvironmentEnum, Settings
from .development import DevelopmentSettings
from .local import LocalSettings
from .production import ProductionSettings
from .testing import TestingsSettings


class SettingsManager:
    """
    Manages the settings based on the provided environment.

    Attributes
    ----------
        environment (str): The specified environment.
        settings (Settings): The settings corresponding to the environment.

    Class Attributes:
        SETTINGS_CLASS_DICT (dict): Mapping of environment values to their respective settings classes.
    """

    SETTINGS_CLASS_DICT: ClassVar = {
        EnvironmentEnum.LOCAL: LocalSettings,
        EnvironmentEnum.DEVELOPMENT: DevelopmentSettings,
        EnvironmentEnum.PRODUCTION: ProductionSettings,
        EnvironmentEnum.TESTING: TestingsSettings,
    }

    def __init__(self, environment: str) -> None:
        """
        Initialize the SettingsManager for the given environment.

        Parameters
        ----------
            environment (str): The specified environment.
        """
        self.environment = environment
        self.settings = self._get_settings()
        self._show_project_info()
        self._configure_logs()
        self._initialize_third_apps()

    def _show_project_info(self) -> None:
        logger.info(f"ENVIRONMENT: {self.settings.ENVIRONMENT} | VERSION: {self.settings.VERSION}")

    def _configure_logs(self) -> None:
        log_level = "DEBUG" if self.settings.DEBUG else "INFO"
        logger.add(
            sys.stdout, colorize=self.settings.COLORIZE_LOG, level=log_level, serialize=self.settings.SERIALIZE_LOG
        )

    def _initialize_third_apps(self) -> None:
        if self.environment in [EnvironmentEnum.DEVELOPMENT, EnvironmentEnum.PRODUCTION]:
            sentry_sdk.init(
                dsn=self.settings.SENTRY_DSN,
                environment=self.settings.ENVIRONMENT,
                traces_sample_rate=0,
                integrations=[FastApiIntegration()],
            )

    def _get_settings(self) -> Settings:
        """
        Fetch the settings class based on the environment.

        Returns
        -------
            Settings: An instance of the settings class corresponding to the environment.

        Raises
        ------
            ValueError: If the environment value is unrecognized.
        """
        try:
            settings_class = self.SETTINGS_CLASS_DICT[self.environment]
        except KeyError as error:
            msg = f"Unrecognized environment value: {self.environment}"
            raise ValueError(msg) from error
        return settings_class()


settings: Settings = SettingsManager(environment=ENVIRONMENT).settings
