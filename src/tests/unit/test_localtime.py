from datetime import date, datetime

from utils.localtime import LocalTime


def test_now() -> None:
    assert LocalTime.now() is not None
    assert isinstance(LocalTime.now(), datetime)


def test_today() -> None:
    assert LocalTime.today() is not None
    assert isinstance(LocalTime.today(), date)


def test_utc_now() -> None:
    assert LocalTime.utcnow() is not None
    assert isinstance(LocalTime.utcnow(), datetime)
