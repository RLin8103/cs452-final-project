import threading
import time
import redis

# Redis Connection
redis_host = 'localhost'
redis_port = 6379
redis_cache = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def critical_section():
    lock_key = "nba_data_fetch_lock"
    try:
        if redis_cache.set(lock_key, "locked", nx=True, ex=10):  # Acquire lock
            print(f"Lock acquired by {threading.current_thread().name}")
            time.sleep(2)  # Simulate a critical operation
        else:
            print(f"Lock unavailable for {threading.current_thread().name}")
    finally:
        redis_cache.delete(lock_key)  # Release lock

def simulate_concurrent_operations():
    threads = [threading.Thread(target=critical_section) for _ in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    simulate_concurrent_operations()
