from enum import StrEnum
from functools import wraps

from fastapi_limiter.depends import RateLimiter


class ThrottleTypeEnum(StrEnum):
    AUTH = "auth"
    PUBLIC = "public"


async def auth_throttle():
    return RateLimiter(times=10, minutes=1)


async def over_load_throttle():
    return RateLimiter(times=1000, minutes=1)


def rate_limit(throttle_type: ThrottleTypeEnum):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if throttle_type == ThrottleTypeEnum.AUTH:
                await auth_throttle()
            else:
                await over_load_throttle()
            return await func(*args, **kwargs)

        return wrapper

    return decorator
