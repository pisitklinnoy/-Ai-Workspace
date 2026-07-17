import asyncio
import sys
import os

# Add backend directory to sys.path to import core.config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arq import create_pool
from arq.connections import RedisSettings
from core.config import settings

async def main():
    # Connect to local Redis instance
    redis = await create_pool(RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT))
    
    # Enqueue the job named 'simple_work' with some test data
    job = await redis.enqueue_job('simple_work', 'Hello ARQ Job!')
    print(f"Enqueued job ID: {job.job_id}")
    
    # Wait for the worker to process the job and return the result
    result = await job.result(timeout=5)
    print(f"Job result received: {result}")

if __name__ == "__main__":
    asyncio.run(main())
