# main.py
from application.cli import main

def handler(event, context):
    main(event)
    return {
        "statusCode": 200,
        "body": "Success"
    }

if __name__ == "__main__":
    main()