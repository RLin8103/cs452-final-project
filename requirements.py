import pandas as pd
from pymongo import MongoClient
import redis
import json
from datetime import timedelta

# Redis Connection (Caching Layer)
redis_host = 'localhost'
redis_port = 6379
redis_cache = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# MongoDB Connection
db_username = 'peterhu4000'
db_password = 'D4mnNvBXwXtAlzbc'
connection_uri = f'mongodb+srv://{db_username}:{db_password}@cs452.llxgy.mongodb.net/?retryWrites=true&w=majority&appName=cs452'
client = MongoClient(connection_uri)

# Database Name
db_name = "NBABASKETBALL"
db = client[db_name]

# List of collection names
collection_names = [
    "common_player_info",
    "draft_combine_stats",
    "draft_history",
    "game_info",
    "game_summary",
    "inactive_players",
    "officials",
    "other_stats",
    "play_by_play",
    "player",
    "team",
    "team_details",
    "team_history"
]

# Function to fetch data from MongoDB with Redis caching
def fetch_nba_data(collection_name):
    cache_key = f"nba:{collection_name}"
    # Check Redis cache
    if redis_cache.exists(cache_key):
        print(f"Fetching {collection_name} data from Redis cache...")
        return json.loads(redis_cache.get(cache_key))

    print(f"Fetching {collection_name} data from MongoDB...")
    collection = db[collection_name]
    data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's internal _id field
    if data:
        # Cache the data in Redis with a TTL of 10 minutes
        redis_cache.setex(cache_key, timedelta(minutes=10), json.dumps(data))
        return data
    else:
        print(f"No data found in MongoDB for collection {collection_name}.")
        return []

# Concurrency control using Redis lock
def critical_operation_with_lock(lock_key, operation, *args, **kwargs):
    try:
        # Acquire lock
        if redis_cache.set(lock_key, "locked", nx=True, ex=10):
            print("Lock acquired. Performing critical operation...")
            operation(*args, **kwargs)  # Execute the critical operation
        else:
            print("Another process is performing this operation. Try again later.")
    finally:
        # Release lock
        redis_cache.delete(lock_key)

# Main function to process and display data
def main():
    # Test Redis and MongoDB connection
    try:
        print("Testing MongoDB connection...")
        print("Databases available:", client.list_database_names())

        # Test Redis connection
        redis_cache.set("test_key", "test_value", ex=10)
        print("Redis test successful:", redis_cache.get("test_key"))
    except Exception as e:
        print(f"Error connecting to Redis or MongoDB: {e}")
        return

    # Fetch data from each collection and display a sample
    for collection_name in collection_names:
        try:
            data = fetch_nba_data(collection_name)
            if data:
                print(f"\nSample data from {collection_name} collection:\n", data[:2])  # Display first 2 records
        except Exception as e:
            print(f"Error fetching data for collection {collection_name}: {e}")

# Perform critical operation with a lock to prevent concurrency issues
critical_operation_with_lock("nba_data_fetch_lock", main)

print("\nData fetch and caching complete.")
