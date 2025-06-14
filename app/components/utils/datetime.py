from datetime import datetime, UTC

def utcnow():
    return datetime.now(UTC)

def now():
    return datetime.now()

def to_unix_timestamp(date: datetime) -> int:
    return int(date.timestamp())

def from_unix_timestamp(stamp: int):
    return datetime.fromtimestamp(stamp)
