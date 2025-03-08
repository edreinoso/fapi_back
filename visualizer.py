from datetime import datetime, timezone
from dynamo_handler import DynamoDBHandler
import matplotlib.pyplot as plt
import numpy as np

# Initialize the handler
ddb_handler = DynamoDBHandler('manual-fapi-ddb')

def visualize_data_in_matplotlib(player_data: dict, attributes: str):
    plt.figure(figsize=(10, 5))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Different colors for attributes
    line_styles = ['-', '--', '-.', ':']  # Different line styles for variation

    for player_index, (player_name, player_stats) in enumerate(player_data.items()):
        if not player_stats:
            continue # Skip players with no data
        
        color = colors[player_index % len(colors)]  # Assign a color per player

        for attr_index, attribute in enumerate(attributes):
            values = [int(d.get(attribute, 0)) for d in player_stats]

            matches = np.arange(1, len(values) + 1)
            linestyle = line_styles[attr_index % len(line_styles)] # Cycle through line styles

            plt.plot(matches, values, marker='o', linestyle=linestyle, color=color, label=f"{player_name} - {attribute}")

    plt.xlabel("Match Round")
    plt.ylabel(attribute.capitalize())  # Dynamic label based on chosen attribute
    plt.title(f"Comparison of {', '.join(attributes).capitalize()} per Match Round")
    plt.xticks(matches)
    plt.legend()
    plt.grid(True)

    plt.show()

def read_player_from_ddb(player_names: dict, attribute: str) -> dict:
    player_data = {}
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format

    print(today)

    for name in player_names:
        response = ddb_handler.query_player_data(name, attribute, today)
        player_data[name] = response

    return player_data

if __name__ == "__main__":
    """Query items in ddb database"""
    # 🌟 Welcoming message
    print("\n⚽ Welcome to the UEFA Fantasy Data Explorer! ⚽")
    print("You can retrieve stats for any player!\n")

    # k. mbappé, rodrydgo

    # 📝 User input for player name and attribute
    player_name = input("Enter player names (comma-separated): ").strip().split(', ')
    attributes = input("Enter the attribute to retrieve (e.g., goals, assists, points): ").strip().split(', ')
    attributes_str = ', '.join(attributes)  # Convert list back into a string
    data = read_player_from_ddb(player_name, attributes_str)

    print(data)

    if data:
        visualize_data_in_matplotlib(data, attributes)  # Pass the dictionary to the function
    else:
        print("No data found for the given players.")
