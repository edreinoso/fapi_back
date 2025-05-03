import matplotlib.pyplot as plt
import numpy as np

def main(event):
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