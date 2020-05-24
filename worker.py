'''
rq worker job configuration
'''
import os

import redis
from rq import Worker, Queue, Connection


listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)


if __name__ == '__main__':
    # for tracking worker job in a terminal
    # assumptions: redis-server is running
    try:
        with Connection(conn):
            worker = Worker(map(Queue, listen))
            print(worker)
            print(list(map(Queue, listen)))
            print(map(Queue, listen))
            print(f"worker name: {worker.name}")
            print(f"host: {worker.hostname}")
            print(f"pid: {worker.pid}")
            print(f"queues: {worker.queues}")
            print(f"state: {worker.state}")
            # print(f"current job: {worker.current_job}")
            print(f"birth: {worker.birth_date}")
            # print(f"last beat: {worker.last_heartbeat}")
            print(f"successful jobs: {worker.successful_job_count}")
            print(f"failed jobs: {worker.failed_job_count}")
            print(f"time alive: {worker.total_working_time}")

            worker.work()
            print("starting work...")
    except Exception as e:
        print(f"{str(e)}")
