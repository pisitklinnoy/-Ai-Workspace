import asyncio
from arq.connections import RedisSettings
from core.config import settings

# Function that displays the job data when executed by the worker
async def simple_work(ctx, data):
    print(f"Executing simple_work with job data: {data}")
    return f"Processed: {data}"

# ARQ Worker settings configuration
class WorkerSettings:
    functions = [simple_work]
    redis_settings = RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT
    )
