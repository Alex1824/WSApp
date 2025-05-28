# Initialize global player names
player1_name = "Player 1"
player2_name = "Player 2"

def set_player_name(player_number: int, name: str):
    """
    Sets the name for player 1 or player 2.

    Args:
        player_number (int): The player number (1 or 2).
        name (str): The name to set for the player.
    """
    global player1_name, player2_name

    if player_number == 1:
        player1_name = name
        print(f"Player 1's name set to: {player1_name}")
    elif player_number == 2:
        player2_name = name
        print(f"Player 2's name set to: {player2_name}")
    else:
        print("Invalid player number. Please use 1 or 2.")

if __name__ == '__main__':
    # Example Usage
    print(f"Initial names: P1='{player1_name}', P2='{player2_name}'")

    set_player_name(1, "Alice")
    set_player_name(2, "Bob")

    print(f"After changes: P1='{player1_name}', P2='{player2_name}'")

    set_player_name(3, "Charlie") # Invalid player number example
    print(f"After invalid attempt: P1='{player1_name}', P2='{player2_name}'")

    set_player_name(1, "Alpha")
    print(f"P1 changed again: P1='{player1_name}', P2='{player2_name}'")
