# Global variables (placeholders, assuming they are managed by the UI/main game loop)
board_size = 3 # Define board_size
board_state = [["" for _ in range(board_size)] for _ in range(board_size)] 
current_player = "X"  # X always starts
game_over = False

# Assume player1_name and player2_name are accessible globally
# from player_setup import player1_name, player2_name # If in a separate file as previously discussed
player1_name = "Player 1" # Placeholder
player2_name = "Player 2" # Placeholder

winner_message = "" # Stores the win/tie message

# UI element placeholders (these would be actual UI widgets in a real application)
class PlaceholderButton:
    def __init__(self):
        self.text_display = ""
        self.disabled_state = False

    def set_text(self, text_value):
        self.text_display = text_value
        print(f"Button text set to: {text_value}")

    def disable(self):
        self.disabled_state = True
        print(f"Button ({self.text_display if self.text_display else 'empty'}) disabled.")

    def enable(self): # Added enable method
        self.disabled_state = False
        print(f"Button ({self.text_display if self.text_display else 'empty'}) enabled.")

class PlaceholderLabel:
    def __init__(self, initial_text=""):
        self.text = initial_text
        print(f"Label text set to: {self.text}")

    def set_text(self, text_value): # Consistent method name
        self.text = text_value
        print(f"Label text updated to: {self.text}")

buttons = [[PlaceholderButton() for _ in range(3)] for _ in range(3)]
turn_label = PlaceholderLabel(f"{player1_name}'s turn (X)")


# Assumed functions (defined elsewhere)
def check_win():
    """Placeholder for checking win condition."""
    # This would check board_state for a win by current_player
    print(f"Checking win for {current_player}")
    # Example: if board_state has three current_player marks in a row, return True
    return False # Default placeholder behavior

def check_tie():
    """
    Checks if the Tic-Tac-Toe game is a tie.
    Assumes check_win() has already been called for the current player.
    Returns:
        bool: True if the game is a tie, False otherwise.
    """
    global board_state
    # print("Checking for a tie (real implementation)") # Optional: for debugging
    for row in board_state:
        for cell in row:
            if cell == "":
                # If any cell is empty, it's not a tie
                return False
    # If all cells are filled (and check_win() was false), it's a tie
    return True

def disable_buttons():
    """
    Disables all buttons on the Tic-Tac-Toe game board.
    Assumes `buttons` is a 2D list of button objects,
    and each button object has a `disable()` method.
    """
    global buttons
    
    if not buttons or not isinstance(buttons, list):
        print("Error: Buttons list is not initialized or is not a list.")
        return

    print("Disabling all game board buttons...")
    disabled_count = 0
    for i, row in enumerate(buttons):
        if not isinstance(row, list):
            print(f"Warning: Row {i} is not a list. Skipping.")
            continue
        for j, button in enumerate(row):
            try:
                # Assuming button objects have a 'disable()' method as per PlaceholderButton
                if hasattr(button, 'disable') and callable(button.disable):
                    button.disable()
                    disabled_count += 1
                else:
                    print(f"Warning: Button at ({i},{j}) does not have a disable method or it's not callable.")
            except Exception as e:
                print(f"Error disabling button at ({i},{j}): {e}")
    print(f"Disabled {disabled_count} buttons.")


def reset_game():
    """
    Resets the Tic-Tac-Toe game to its initial state.
    """
    global board_state, buttons, current_player, game_over, winner_message, turn_label, player1_name, board_size
    
    print("Resetting game...")

    # 1. Reset board_state
    board_state = [["" for _ in range(board_size)] for _ in range(board_size)]
    print("Board state reset.")

    # 2. Reset buttons visual state
    if buttons and isinstance(buttons, list):
        reset_buttons_count = 0
        for i, row in enumerate(buttons):
            if isinstance(row, list):
                for j, button in enumerate(row):
                    try:
                        if hasattr(button, 'set_text') and callable(button.set_text):
                            button.set_text("")
                        if hasattr(button, 'enable') and callable(button.enable):
                            button.enable()
                        reset_buttons_count +=1
                    except Exception as e:
                        print(f"Error resetting button at ({i},{j}): {e}")
        print(f"Reset and enabled {reset_buttons_count} buttons.")
    else:
        print("Warning: Buttons list not found or not a list, cannot reset button visuals.")

    # 3. Reset game state variables
    current_player = "X"
    game_over = False
    winner_message = ""
    print(f"Game state variables reset. Current player: {current_player}, Game over: {game_over}")

    # 4. Update turn_label
    if hasattr(turn_label, 'set_text') and callable(turn_label.set_text):
        initial_turn_message = f"{player1_name}'s turn (X)"
        turn_label.set_text(initial_turn_message)
        print(f"Turn label updated to: {initial_turn_message}")
    else:
        print("Warning: turn_label does not have a set_text method.")
    
    print("Game reset complete.")


# Main function to be implemented
def handle_click(row: int, col: int):
    """
    Handles a click on a square of the Tic-Tac-Toe board.
    """
    global board_state, current_player, game_over, buttons, turn_label, player1_name, player2_name, winner_message

    if game_over:
        print("Game is over. No more moves allowed.")
        return
    
    if board_state[row][col] != "":
        print(f"Cell ({row},{col}) is already taken by {board_state[row][col]}.")
        return

    # Update board state and button text
    board_state[row][col] = current_player
    buttons[row][col].set_text(current_player)
    buttons[row][col].disable()
    print(f"Player {current_player} marked cell ({row},{col}). Board state updated.")

    # Check for win
    if check_win():
        game_over = True
        winner_name = player1_name if current_player == "X" else player2_name
        winner_message = f"{winner_name} wins!"
        turn_label.set_text(winner_message)
        print(winner_message)
        disable_buttons()
        return

    # Check for tie
    if check_tie():
        game_over = True
        winner_message = "It's a tie!"
        turn_label.set_text(winner_message)
        print(winner_message)
        disable_buttons()
        return

    # Switch player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"
    
    next_player_name = player1_name if current_player == "X" else player2_name
    turn_label.set_text(f"{next_player_name}'s turn ({current_player})")
    print(f"Turn switched. It's now {next_player_name}'s turn ({current_player}).")


if __name__ == '__main__':
    # Example Usage Flow
    print("--- Game Start ---")
    print(f"Initial turn: {turn_label.text}")

    # Simulate some moves
    handle_click(0, 0) # P1 (X)
    # Expected: Player X marked cell (0,0). Board state updated.
    # Expected: Turn switched. It's now Player 2's turn (O).
    
    handle_click(1, 1) # P2 (O)
    # Expected: Player O marked cell (1,1). Board state updated.
    # Expected: Turn switched. It's now Player 1's turn (X).

    handle_click(0, 0) # Attempt to click already taken cell
    # Expected: Cell (0,0) is already taken by X.
    
    handle_click(0, 1) # P1 (X)
    
    # Simulate a winning condition by overriding check_win for testing
    def mock_check_win_for_X():
        global current_player
        if current_player == "X": # Assume X just made a winning move
            print("Mock check_win: X wins!")
            return True
        return False

    original_check_win = check_win # Save original
    check_win = mock_check_win_for_X 
    
    handle_click(0, 2) # P1 (X) makes a "winning" move
    # Expected: Player X marked cell (0,2). Board state updated.
    # Expected: Mock check_win: X wins!
    # Expected: Player 1 wins!
    # Expected: Disabling all game board buttons.
    
    print(f"Game over state: {game_over}")
    print(f"Final message: {winner_message}")

    handle_click(1, 0) # Attempt move after game over
    # Expected: Game is over. No more moves allowed.

    # Reset for tie game example
    board_state = [["" for _ in range(3)] for _ in range(3)]
    buttons = [[PlaceholderButton() for _ in range(3)] for _ in range(3)] # Re-initialize buttons
    current_player = "X"
    game_over = False
    winner_message = ""
    turn_label = PlaceholderLabel(f"{player1_name}'s turn (X)")
    check_win = original_check_win # Restore original check_win
    
    # Test the real check_tie function
    print("\n--- Tie Game Simulation (Real check_tie) ---")
    board_state = [["X", "O", "X"], 
                   ["X", "O", "O"], 
                   ["O", "X", ""]] # Almost full, X to move
    # Update button states to match board_state for consistency in this test
    for r_idx, r_val in enumerate(board_state):
        for c_idx, c_val in enumerate(r_val):
            if c_val:
                buttons[r_idx][c_idx].set_text(c_val)
                buttons[r_idx][c_idx].disable()
            else:
                buttons[r_idx][c_idx].text_display = ""
                buttons[r_idx][c_idx].disabled_state = False


    current_player = "X"
    game_over = False
    winner_message = ""
    turn_label.set_text(f"{player1_name}'s turn (X)")
    
    print("Board before potential tie move:")
    for r in board_state: print(r)
    
    handle_click(2, 2) # X makes the final move, filling the board
    # Expected: Player X marked cell (2,2). Board state updated.
    # Expected: Checking win for X (will be false with original check_win)
    # Expected: (If check_tie is called and works) It's a tie!
    # Expected: (If check_tie is called and works) Disabling all game board buttons.

    print("Board after potential tie move:")
    for r in board_state: print(r)
    print(f"Game over state: {game_over}")
    print(f"Final message: {winner_message}")

    # Test case: Not a tie yet
    print("\n--- Not a Tie Yet Simulation ---")
    board_state = [["X", "O", ""], ["", "X", ""], ["", "", "O"]]
    current_player = "X"
    game_over = False # Ensure game_over is False for this test
    winner_message = ""
    turn_label.set_text(f"{player1_name}'s turn (X)")
    print("Board state (not a tie):")
    for r in board_state: print(r)
    if not check_tie(): # Direct call for testing
        print("Correctly identified as not a tie yet.")
    else:
        print("Incorrectly identified as a tie.")
    
    # Test reset_game functionality
    print("\n--- Reset Game Test ---")
    # Make some moves to change state
    handle_click(1,2) # X
    handle_click(2,0) # O
    
    print("State before reset:")
    print(f"Board: {board_state}")
    print(f"Current Player: {current_player}")
    print(f"Game Over: {game_over}")
    print(f"Turn Label: {turn_label.text}")
    
    reset_game()
    
    print("State after reset:")
    print(f"Board: {board_state}")
    print(f"Current Player: {current_player}")
    print(f"Game Over: {game_over}")
    print(f"Turn Label: {turn_label.text}")
    # Verify button states (first button as sample)
    print(f"Button (0,0) text: '{buttons[0][0].text_display}', disabled: {buttons[0][0].disabled_state}")
    
    # Simulate a win, then reset
    print("\n--- Win and Reset Test ---")
    check_win = mock_check_win_for_X # Use the mock win function
    handle_click(0,0) # X
    handle_click(1,0) # O
    handle_click(0,1) # X
    handle_click(1,1) # O
    handle_click(0,2) # X wins
    
    print("State after win:")
    print(f"Board: {board_state}")
    print(f"Current Player: {current_player}") # Should be X (winner)
    print(f"Game Over: {game_over}") # Should be True
    print(f"Winner Message: {winner_message}")
    print(f"Turn Label: {turn_label.text}")
    
    reset_game()
    check_win = original_check_win # Restore original check_win function
    
    print("State after reset (post-win):")
    print(f"Board: {board_state}")
    print(f"Current Player: {current_player}")
    print(f"Game Over: {game_over}")
    print(f"Winner Message: {winner_message}")
    print(f"Turn Label: {turn_label.text}")
    print(f"Button (0,2) text: '{buttons[0][2].text_display}', disabled: {buttons[0][2].disabled_state}")
