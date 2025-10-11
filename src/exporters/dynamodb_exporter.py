"""
DynamoDB export functionality for UEFA Champions League data
"""
import boto3
import logging
from typing import List, Dict, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError


class DynamoDBExporter:
    """Handles exporting data to DynamoDB tables"""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name
        self.logger = logging.getLogger(__name__)
        self._dynamodb = None
    
    @property
    def dynamodb(self):
        """Lazy initialization of DynamoDB client"""
        if self._dynamodb is None:
            try:
                self._dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
                self.logger.info(f"DynamoDB client initialized for region {self.region_name}")
            except NoCredentialsError:
                self.logger.error("AWS credentials not found. Please configure your AWS credentials.")
                raise
            except Exception as e:
                self.logger.error(f"Error initializing DynamoDB client: {str(e)}")
                raise
        return self._dynamodb
    
    def create_players_table_if_not_exists(self, table_name: str = "uefa-players") -> bool:
        """
        Create the players table if it doesn't exist
        
        Args:
            table_name: Name of the DynamoDB table
            
        Returns:
            True if table exists or was created successfully, False otherwise
        """
        try:
            # Check if table exists
            table = self.dynamodb.Table(table_name)
            table.load()
            self.logger.info(f"Table '{table_name}' already exists")
            return True
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                # Table doesn't exist, create it
                self.logger.info(f"Creating table '{table_name}'")
                
                try:
                    table = self.dynamodb.create_table(
                        TableName=table_name,
                        KeySchema=[
                            {
                                'AttributeName': 'playerId',
                                'KeyType': 'HASH'  # Partition key
                            }
                        ],
                        AttributeDefinitions=[
                            {
                                'AttributeName': 'playerId',
                                'AttributeType': 'S'  # String
                            }
                        ],
                        BillingMode='PAY_PER_REQUEST'  # On-demand billing
                    )
                    
                    # Wait for table to be created
                    table.wait_until_exists()
                    self.logger.info(f"Table '{table_name}' created successfully")
                    return True
                    
                except ClientError as create_error:
                    self.logger.error(f"Error creating table '{table_name}': {create_error}")
                    return False
            else:
                self.logger.error(f"Error checking table '{table_name}': {e}")
                return False
    
    def export_players_data(self, players_data: List[Dict[str, Any]], table_name: str = "uefa-players") -> bool:
        """
        Export players data to DynamoDB table
        
        Args:
            players_data: List of player data dictionaries
            table_name: Name of the DynamoDB table
            
        Returns:
            True if export successful, False otherwise
        """
        self.logger.info(f"Exporting {len(players_data)} players to DynamoDB table '{table_name}'")
        
        if not players_data:
            self.logger.error("No players data to export")
            return False
        
        # Ensure table exists
        if not self.create_players_table_if_not_exists(table_name):
            return False
        
        try:
            table = self.dynamodb.Table(table_name)
            successful_writes = 0
            failed_writes = 0
            
            # Write items to DynamoDB
            with table.batch_writer() as batch:
                for player in players_data:
                    try:
                        # Prepare item for DynamoDB
                        item = self._prepare_player_item(player)
                        batch.put_item(Item=item)
                        successful_writes += 1
                        
                    except Exception as e:
                        self.logger.warning(f"Failed to write player {player.get('name', 'unknown')}: {str(e)}")
                        failed_writes += 1
            
            self.logger.info(f"Successfully exported {successful_writes} players to DynamoDB")
            if failed_writes > 0:
                self.logger.warning(f"Failed to export {failed_writes} players")
            
            return failed_writes == 0  # Return True only if all writes succeeded
            
        except ClientError as e:
            self.logger.error(f"Error writing to DynamoDB table '{table_name}': {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during DynamoDB export: {str(e)}")
            return False
    
    def _prepare_player_item(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare player data for DynamoDB storage
        
        Args:
            player: Player data dictionary
            
        Returns:
            Prepared item for DynamoDB
        """
        # Convert all values to strings and handle None values
        item = {}
        
        for key, value in player.items():
            if value is None or value == "":
                item[key] = "N/A"
            else:
                # Convert all values to strings for consistency
                item[key] = str(value)
        
        # Ensure playerId exists (required for partition key)
        if 'playerId' not in item or not item['playerId']:
            # Generate a fallback playerId if missing
            item['playerId'] = f"player_{item.get('name', 'unknown').replace(' ', '_').lower()}"
        
        return item
    
    def get_player_by_id(self, player_id: str, table_name: str = "uefa-players") -> Optional[Dict[str, Any]]:
        """
        Retrieve a player by ID from DynamoDB
        
        Args:
            player_id: The player ID to lookup
            table_name: Name of the DynamoDB table
            
        Returns:
            Player data dictionary or None if not found
        """
        try:
            table = self.dynamodb.Table(table_name)
            response = table.get_item(Key={'playerId': player_id})
            
            if 'Item' in response:
                self.logger.info(f"Retrieved player {player_id} from DynamoDB")
                return response['Item']
            else:
                self.logger.info(f"Player {player_id} not found in DynamoDB")
                return None
                
        except ClientError as e:
            self.logger.error(f"Error retrieving player {player_id}: {e}")
            return None
    
    def list_all_players(self, table_name: str = "uefa-players") -> List[Dict[str, Any]]:
        """
        Retrieve all players from DynamoDB table
        
        Args:
            table_name: Name of the DynamoDB table
            
        Returns:
            List of all player data dictionaries
        """
        try:
            table = self.dynamodb.Table(table_name)
            response = table.scan()
            
            players = response.get('Items', [])
            
            # Handle pagination if there are more items
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                players.extend(response.get('Items', []))
            
            self.logger.info(f"Retrieved {len(players)} players from DynamoDB")
            return players
            
        except ClientError as e:
            self.logger.error(f"Error scanning DynamoDB table '{table_name}': {e}")
            return []