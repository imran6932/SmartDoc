import os
import redis
from fastapi import HTTPException
from datetime import datetime

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0, decode_responses=True)

DAILY_LIMITS = {
    "uploads": int(os.getenv("UPLOAD_LIMIT", 3)),
    "chats": int(os.getenv("CHAT_LIMIT", 12))
}


def check_limit(ip: str, action: str):
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"{ip}:{action}:{today}"

    count = r.get(key)
    count = int(count) if count else 0

    limit = DAILY_LIMITS[action]

    if count >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Daily limit of {limit} {action} reached. Try again tomorrow."
        )

    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, 86400)
    pipe.execute()