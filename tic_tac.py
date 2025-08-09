import math
import tkinter as tk
from tkinter import messagebox

# Constants
HUMAN = 'X'
AI = 'O'
EMPTY = ' '

# Game variables
board = [[EMPTY for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
use_alpha_beta = True

# Color Palette
BACKGROUND_COLOR = '#ffebee'  # Soft pastel background
BUTTON_COLOR = '#ffffff'        # Button color
BUTTON_HOVER_COLOR = '#f8bbd0'  # Button hover color
PLAYER_COLOR = '#ff4081'        # Player color
AI_COLOR = '#3f51b5'            # AI color
RESET_BUTTON_COLOR = '#4caf50'  # Reset button color
RESET_BUTTON_TEXT_COLOR = '#ffffff'  # Reset button text color

# Evaluation logic
def evaluate():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return 1 if board[i][0] == AI else -1
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return 1 if board[0][i] == AI else -1

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return 1 if board[0][0] == AI else -1
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return 1 if board[0][2] == AI else -1

    return 0

def is_moves_left():
    return any(EMPTY in row for row in board)

# Minimax with optional Alpha-Beta Pruning
def minimax(depth, is_max):
    score = evaluate()
    if score != 0 or not is_moves_left():
        return score

    best = -math.inf if is_max else math.inf
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI if is_max else HUMAN
                move_val = minimax(depth + 1, not is_max)
                board[i][j] = EMPTY
                best = max(best, move_val) if is_max else min(best, move_val)
    return best

def minimax_ab(depth, is_max, alpha, beta):
    score = evaluate()
    if score != 0 or not is_moves_left():
        return score

    best = -math.inf if is_max else math.inf
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI if is_max else HUMAN
                val = minimax_ab(depth + 1, not is_max, alpha, beta)
                board[i][j] = EMPTY
                if is_max:
                    best = max(best, val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
                else:
                    best = min(best, val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
    return best

# AI Move
def best_move():
    best_val = -math.inf
    move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax_ab(0, False, -math.inf, math.inf) if use_alpha_beta else minimax(0, False)
                board[i][j] = EMPTY
                if move_val > best_val:
                    move = (i, j)
                    best_val = move_val
    return move

# Handle player's click
def on_click(i, j):
    if board[i][j] != EMPTY:
        return

    board[i][j] = HUMAN
    buttons[i][j].config(text=HUMAN, fg=PLAYER_COLOR, state='disabled', disabledforeground=PLAYER_COLOR)

    if evaluate() == -1:
        end_game("You win! 🎉")
        return
    if not is_moves_left():
        end_game("It's a draw!")
        return

    # AI Move
    ai_i, ai_j = best_move()
    board[ai_i][ai_j] = AI
    buttons[ai_i][ai_j].config(text=AI, fg=AI_COLOR, state='disabled', disabledforeground=AI_COLOR)

    if evaluate() == 1:
        end_game("AI wins! 🤖")
    elif not is_moves_left():
        end_game("It's a draw!")

def end_game(msg):
    messagebox.showinfo("Game Over", msg)
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state='disabled')

def reset_game():
    global board
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=EMPTY, fg='black', state='normal')

# GUI Setup
root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.configure(bg=BACKGROUND_COLOR)

frame = tk.Frame(root, bg=BACKGROUND_COLOR, padx=10, pady=10)
frame.pack(expand=True)

style = {
    'font': ('Helvetica', 48, 'bold'),
    'width': 5,
    'height': 2,
    'bg': BUTTON_COLOR,
    'activebackground': BUTTON_HOVER_COLOR,
    'relief': 'raised',
    'bd': 5
}

def on_enter(button):
    button.config(bg=BUTTON_HOVER_COLOR)

def on_leave(button):
    button.config(bg=BUTTON_COLOR)

for i in range(3):
    for j in range(3):
        button = tk.Button(frame, text=EMPTY, **style, command=lambda i=i, j=j: on_click(i, j))
        button.grid(row=i, column=j, padx=5, pady=5)
        button.bind("<Enter>", lambda e, b=button: on_enter(b))
        button.bind("<Leave>", lambda e, b=button: on_leave(b))
        buttons[i][j] = button

reset_button = tk.Button(root, text="Reset Game", font=('Helvetica', 16, 'bold'), bg=RESET_BUTTON_COLOR, 
                         fg=RESET_BUTTON_TEXT_COLOR, padx=10, pady=5, command=reset_game)
reset_button.pack(pady=20)

root.mainloop()
