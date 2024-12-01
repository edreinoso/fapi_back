# UCL Fantasy

This project is designed to update player data in a Notion database using data fetched from the UEFA gaming hub. The script performs the following tasks:

1. **Fetch Player Data**: Retrieves player data from the UEFA gaming hub endpoint.
2. **Download Existing Entries**: Downloads existing entries from an S3 bucket.
3. **Update Notion Database**: Updates the Notion database with the new player data.
4. **Generate CSV File**: Generates a CSV file with the updated player data.

## Requirements

- Python 3.11
- `requests` library
- `boto3` library

## Setup

1. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Set up your Notion API credentials and S3 bucket details in the script.

## Usage

1. Run the script to update the Notion database and generate the CSV file:
    ```sh
    python script.py
    ```

## Files

- `script.py`: Main script to fetch player data, update Notion database, and generate CSV file.
- `notion.py`: Contains the `Notion` class to interact with the Notion API.
- `requirements.txt`: Lists the required Python libraries.

## Configuration

- Update the Notion API credentials and S3 bucket details in the `Notion` class in [`notion.py`](../ucl_fantasy/notion.py).
- Modify the field names and data processing logic as needed in the `csv_table` function in [`script.py`](../ucl_fantasy/script.py).

## License

This project is licensed under the MIT License.