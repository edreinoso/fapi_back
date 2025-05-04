import datetime
from ports.ddb_port import DDBPlayerStatsRepository

class MeasurementService:
    def __init__(self, measurement_repository: DDBPlayerStatsRepository, memory_capacity: int, execution_location: str, execution_method: str, access_pattern: str):
        self.measurement_repository = measurement_repository
        self.uefa_execution_time = 0
        self.ddb_execution_time = 0
        self.total_execution_time = 0
        self.memory_capacity = memory_capacity
        self.number_of_players = 0
        self.average_time_per_player = 0
        self.access_pattern = access_pattern
        self.execution_method = execution_method
        self.execution_location = execution_location
    
    def increment_uefa_execution_time(self, uefa_execution_time: float):
        self.uefa_execution_time += uefa_execution_time

    def update_ddb_with_runtime_measurement(self):
        self.total_execution_time = self.uefa_execution_time + self.ddb_execution_time
        self.measurement_repository.put_measurement_items(
            self.execution_method,
            self.execution_location,
            self.ddb_execution_time,
            self.uefa_execution_time,
            self.total_execution_time,
            self.number_of_players,
            self.access_pattern,
            self.average_time_per_player,
            self.memory_capacity
        )
        self.print_runtime_measurement()

    def print_runtime_measurement(self):
        print(f"\nPlayers recorded: {self.number_of_players}.")
        print(f"Uefa execution time: {self.uefa_execution_time:.2f} seconds.\nDynamoDB execution time: {self.ddb_execution_time:.2f} seconds. \nTotal execution time: {self.total_execution_time:.2f} seconds.\nAverage time per player: {self.average_time_per_player:.2f} seconds.")