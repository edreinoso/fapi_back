from abc import ABC, abstractmethod
from typing import Dict

# This class serves as a base class for DynamoDB items.
# It defines the structure and methods that any DynamoDB item should implement.
# The class is abstract, meaning it cannot be instantiated directly.
# It requires subclasses to implement the pk, sk, and to_item methods.
# The pk method should return the partition key for the item.
# The sk method should return the sort key for the item.
class DynamoDBItem(ABC):
    @property
    @abstractmethod
    def pk(self) -> str:
        pass

    @property
    @abstractmethod
    def sk(self) -> str:
        pass

    def keys(self) -> Dict[str, str]:
        return {
            "PK": self.pk,
            "SK": self.sk
        }

    @abstractmethod
    def to_item(self) -> Dict[str, str]:
        pass