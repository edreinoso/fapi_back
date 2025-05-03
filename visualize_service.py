# This service will be responsible for creating the graphs in matplotlib
# The only disadvatnage is where I want to be using such a heavy library
# in a lambda function, due to the size of the library. That's something
# I still need to think about.

"""
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
"""