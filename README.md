# cs452-final-project

## Upload Kaggle Basketball Dataset to MongoDB Atlas

This project processes and uploads the **Kaggle Basketball Dataset** to a MongoDB Atlas database. The dataset is downloaded, processed, and stored in separate MongoDB collections based on the CSV files.

### Steps to Run the Script

1. **Set Up MongoDB Atlas**

   - Create a MongoDB Atlas cluster.
   - Note your connection string and credentials (`username`, `password`, and `cluster URL`).

2. **Install Dependencies**

   - Ensure you have a Conda environment set up. Activate it and install the required dependencies:
     ```bash
     conda install pandas pymongo
     pip install kagglehub
     ```

3. **Set Up Kaggle API Key**

   - Obtain your Kaggle API key from your Kaggle account ([Kaggle API Documentation](https://www.kaggle.com/docs/api)).
   - Save the `kaggle.json` file to `~/.kaggle/`.

4. **Run the Script**

   - Execute the script to download the dataset and upload it to MongoDB Atlas:
     ```bash
     python upload_kaggle_csv_to_mongo.py
     ```

5. **Verify MongoDB Atlas**
   - Log in to MongoDB Atlas.
   - Navigate to your database (e.g., `NBA`) and check the collections for the uploaded data.

---

### Dataset Details

- **Source**: [Kaggle Basketball Dataset](https://www.kaggle.com/datasets/wyattowalsh/basketball)
- **Structure**:
  - Contains multiple CSV files stored in a `csv` directory.
  - Each CSV represents a separate table, such as `players`, `teams`, and `games`.

---

### Script Highlights

1. **Download Dataset**:

   - Automatically downloads the dataset using `kagglehub`.

2. **Process CSV Files**:

   - Reads each CSV file from the `csv` directory.
   - Converts the data into a dictionary format for MongoDB.

3. **Insert Data into MongoDB**:

   - Creates a MongoDB collection for each CSV file.
   - Inserts the processed data into the respective collection.

4. **Error Handling**:
   - Skips empty files.
   - Handles file reading and MongoDB insertion errors gracefully.

---

### Example Output

When running the script, you should see:

```text
Testing MongoDB connection...
Databases available: ['NBA', 'admin', 'local']
Downloading Kaggle dataset...
Path to dataset files: /Users/username/.cache/kagglehub/datasets/wyattowalsh/basketball/versions/231/csv

Processing file: /path/to/csv/players.csv
Creating collection: players
First few rows of players.csv:
        Player   Team  Points  Assists
0  LeBron James  Lakers     27        8
...
Inserted 500 records into 'players' collection.

Processing file: /path/to/csv/teams.csv
...
Successfully processed and uploaded 3 files.

Data upload complete.
```

---

### Troubleshooting

1. **No Files Processed**:

   - Verify the `kaggle.json` API key is properly configured in `~/.kaggle/`.
   - Check that the `csv` directory exists in the dataset path.

2. **MongoDB Connection Issues**:

   - Confirm the connection URI in the script.
   - Ensure your IP address is whitelisted in MongoDB Atlas.

3. **Missing Data**:
   - Check MongoDB Atlas collections for the inserted data.
   - Validate the CSV files for proper formatting.
