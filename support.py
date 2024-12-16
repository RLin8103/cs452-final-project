import time
from concurrent.futures import ThreadPoolExecutor
import redis
import json

# Redis Connection
redis_host = 'localhost'
redis_port = 6379
redis_cache = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def fetch_from_cache(collection_name):
    start_time = time.time()
    cache_key = f"nba:{collection_name}"
    if redis_cache.exists(cache_key):
        data = redis_cache.get(cache_key)
        elapsed_time = time.time() - start_time
        return elapsed_time
    else:
        return None

def simulate_load(collection_name, num_requests):
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(lambda _: fetch_from_cache(collection_name), range(num_requests)))
    return results

if __name__ == "__main__":
    collection_name = "players"
    num_requests = 5000

    print("Warming up cache...")
    redis_cache.set(f"nba:{collection_name}", json.dumps({"test": "data"}))

    print(f"Simulating {num_requests} requests...")
    latencies = simulate_load(collection_name, num_requests)
    print(f"Average latency: {sum(latencies) / len(latencies):.6f} seconds")
    print(f"Requests with subsecond latency: {sum(1 for l in latencies if l < 1):,}/{num_requests}")
