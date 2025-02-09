from notion_client import Client

class Notion:
    def __init__(self, token, db_id):
        self.db_id = db_id
        self.client = Client(auth=token)

    def write_row(self, name: str):
    # def write_row(self, properties: dict):
        res = self.client.pages.create(
            **{
                "parent": {
                    "database_id": self.db_id
                },
                'properties': {
                    'name': {
                        'title': [
                            {
                                'text': {
                                    'content': name
                                }
                            }
                        ]
                    },
                    'rating': {
                        'number': {
                        }
                    }
                }
            }
        )

        print(res)