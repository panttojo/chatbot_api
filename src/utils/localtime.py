from datetime import UTC, date, datetime

import pytz

from core.settings import settings

DEFAULT_TIMEZONE = settings.TIMEZONE


class LocalTime:
    @staticmethod
    def utcnow() -> datetime:
        """The function `utcnow()` returns the current datetime in Coordinated
        Universal Time (UTC).

        Returns
        -------
            The function `utcnow()` returns the current datetime in Coordinated
        Universal Time (UTC).

        """
        return datetime.now(UTC)

    @staticmethod
    def now(tz: str = DEFAULT_TIMEZONE) -> datetime:
        """The function `now` returns the current datetime in the specified
        timezone.

        Parameters
        ----------
        tz : str
            The `tz` parameter is a string that represents the time zone you want to
        convert the current time to. It is an optional parameter with a default value of
        `TIME_ZONE`.

        Returns
        -------
            the current datetime in the specified timezone.
        """

        now = LocalTime.utcnow()
        local_tz = pytz.timezone(tz)
        return now.astimezone(local_tz)

    @staticmethod
    def today(tz: str = DEFAULT_TIMEZONE) -> date:
        """The function "get_today" returns the current date in the specified time
        zone.

        Parameters
        ----------
        tz : str
            The `tz` parameter is a string that represents the time zone. It is used to
        specify the time zone for which the current date should be returned. The default
        value is `TIME_ZONE`, which is likely a constant or variable defined elsewhere
        in the code.

        Returns
        -------
            the current date in the local time zone.
        """

        local_now = LocalTime.now(tz)
        return local_now.date()
