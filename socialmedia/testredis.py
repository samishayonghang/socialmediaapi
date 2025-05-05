import redis

# Replace with your Redis URL
redis_url ="rediss://red-d0c13ppr0fns73dura5g:yhrASCGgZVH5QBRaz0MSopDyV9JdSQkq@singapore-keyvalue.render.com:6379"

# Create Redis client
client = redis.StrictRedis.from_url(redis_url)

# Test connection
try:
    response = client.ping()  # Should return True if Redis is reachable
    if response:
        print("Redis is connected and working!")
except redis.exceptions.ConnectionError as e:
    print(f"Connection to Redis failed: {e}")
