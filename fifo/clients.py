import redis
from uuid import uuid4

r = redis.Redis(host='localhost', port=6379)

p = r.pubsub(ignore_subscribe_messages=True)
r.publish('my-channel',uuid4())

