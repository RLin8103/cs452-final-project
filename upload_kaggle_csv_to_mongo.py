import kagglehub
import pandas as pd
from pymongo import MongoClient
import os

# MongoDB Connection
db_username = 'peterhu4000'
db_password = 'D4mnNvBXwXtAlzbc'
connection_uri = f'mongodb+srv://{db_username}:{db_password}@cs452.llxgy.mongodb.net/?retryWrites=true&w=majority&appName=cs452'
client = MongoClient(connection_uri)

# Database Name
db_name = "NBABASKETBALL"
db = client[db_name]

# Step 1: Test MongoDB connection
try:
    print("Testing MongoDB connection...")
    print("Databases available:", client.list_database_names())
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Step 2: Download Kaggle Dataset
try:
    print("Downloading Kaggle dataset...")
    path = kagglehub.dataset_download("wyattowalsh/basketball")
    print("Path to dataset files:", path)
except Exception as e:
    print(f"Error downloading dataset: {e}")
    exit()

# Step 3: Locate the 'csv' directory
csv_dir = os.path.join(path, "csv")
if not os.path.exists(csv_dir):
    print(f"'csv' directory not found in {path}. Please check the dataset structure.")
    exit()

# Step 4: Process Each CSV File in the 'csv' Directory
files_processed = 0
for file in os.listdir(csv_dir):
    if file.endswith(".csv"):
        csv_file_path = os.path.join(csv_dir, file)
        collection_name = os.path.splitext(file)[0]  # Use file name (without .csv) as collection name

        print(f"\nProcessing file: {csv_file_path}")
        print(f"Creating collection: {collection_name}")

        try:
            # Load CSV
            data = pd.read_csv(csv_file_path)

            if data.empty:
                print(f"Skipping empty file: {file}")
                continue

            # Preview the first few rows of data
            print(f"First few rows of {file}:\n", data.head())

            # Convert to Dictionary
            data_dict = data.to_dict("records")
            print(f"Number of records to insert: {len(data_dict)}")

            # Insert into MongoDB
            collection = db[collection_name]
            result = collection.insert_many(data_dict)
            print(f"Inserted {len(result.inserted_ids)} records into '{collection_name}' collection.")
            files_processed += 1

        except Exception as e:
            print(f"Error processing file {file}: {e}")

if files_processed == 0:
    print("No files were processed or uploaded.")
else:
    print(f"\nSuccessfully processed and uploaded {files_processed} files.")

print("\nData upload complete.")
