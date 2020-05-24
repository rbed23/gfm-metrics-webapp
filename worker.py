'''
rq worker job configuration
'''
import os, json

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
            worker = Worker(list(map(Queue, listen)))
            print(worker)
            print(list(map(Queue, listen)))

            print(vars(worker))

            worker.work()
            print("starting work...")
    except Exception as e:
        print(f"{str(e)}")
