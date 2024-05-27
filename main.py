import numpy as np
import tkinter as tk
from tkinter import font, messagebox
from tkinter import ttk

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
width = SQUARESIZE * COLUMN_COUNT
height = SQUARESIZE * ROW_COUNT + SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)

# COLORS
BLUE = "#1F51FF"
BLACK = "#000000"
RED = "#FF5733"
YELLOW = "#FFD700"
WHITE = "#FFFFFF"

class Connect4:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Comic Sans MS", 16), padding=10)

        self.font = font.Font(family='Comic Sans MS', size=30, weight='bold')
        
        self.start_screen()

    def start_screen(self):
        self.clear_screen()
        self.label = tk.Label(self.root, text="Who starts the game?", font=("Comic Sans MS", 24, "bold"))
        self.label.pack(pady=20)

        self.red_button = ttk.Button(self.root, text="Red", command=lambda: self.start_game(0), style="TButton")
        self.red_button.pack(side="left", padx=50, pady=20)

        self.yellow_button = ttk.Button(self.root, text="Yellow", command=lambda: self.start_game(1), style="TButton")
        self.yellow_button.pack(side="right", padx=50, pady=20)

    def start_game(self, starter):
        self.clear_screen()
        
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=WHITE, bd=0, highlightthickness=0)
        self.canvas.pack(pady=10)

        self.reset_button = ttk.Button(self.root, text="Reset Game", command=self.reset_game, style="TButton")
        self.reset_button.pack(pady=10)
        
        self.turn = starter
        self.reset_game()

        self.canvas.bind("<Motion>", self.mouseMotion)
        self.canvas.bind("<Button-1>", self.mouseClick)

    def reset_game(self):
        self.gameBoard = self.createBoard()
        self.gameOver = False
        self.canvas.delete("winner")
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                self.canvas.create_rectangle(c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, 
                                             c * SQUARESIZE + SQUARESIZE, r * SQUARESIZE + 2 * SQUARESIZE, 
                                             fill=BLUE, outline=BLACK)
                self.canvas.create_oval(c * SQUARESIZE + 5, r * SQUARESIZE + SQUARESIZE + 5, 
                                        c * SQUARESIZE + SQUARESIZE - 5, r * SQUARESIZE + 2 * SQUARESIZE - 5, 
                                        fill=WHITE, outline=BLACK)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.gameBoard[r][c] == 1:
                    self.canvas.create_oval(c * SQUARESIZE + 5, height - (r * SQUARESIZE + SQUARESIZE - 5),
                                            c * SQUARESIZE + SQUARESIZE - 5, height - (r * SQUARESIZE + 5), 
                                            fill=RED, outline=BLACK)
                elif self.gameBoard[r][c] == 2:
                    self.canvas.create_oval(c * SQUARESIZE + 5, height - (r * SQUARESIZE + SQUARESIZE - 5),
                                            c * SQUARESIZE + SQUARESIZE - 5, height - (r * SQUARESIZE + 5), 
                                            fill=YELLOW, outline=BLACK)

    def createBoard(self):
        return np.zeros((ROW_COUNT, COLUMN_COUNT))

    def isValidLocation(self, board, col):
        return board[ROW_COUNT - 1][col] == 0

    def getNextOpenRow(self, board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    def dropCircle(self, board, row, col, piece):
        board[row][col] = piece

    def winningMove(self, board, piece):
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True

    def mouseMotion(self, event):
        self.canvas.delete("cursor")
        if not self.gameOver:
            posx = event.x
            if self.turn == 0:
                self.canvas.create_oval(posx - RADIUS, SQUARESIZE / 2 - RADIUS, 
                                        posx + RADIUS, SQUARESIZE / 2 + RADIUS, 
                                        fill=RED, outline=BLACK, tags="cursor")
            else:
                self.canvas.create_oval(posx - RADIUS, SQUARESIZE / 2 - RADIUS, 
                                        posx + RADIUS, SQUARESIZE / 2 + RADIUS, 
                                        fill=YELLOW, outline=BLACK, tags="cursor")

    def mouseClick(self, event):
        if not self.gameOver:
            posx = event.x
            col = int(posx // SQUARESIZE)

            if self.isValidLocation(self.gameBoard, col):
                row = self.getNextOpenRow(self.gameBoard, col)
                if self.turn == 0:
                    self.dropCircle(self.gameBoard, row, col, 1)
                    if self.winningMove(self.gameBoard, 1):
                        self.draw_board()
                        self.gameOver = True
                        self.show_winner("RED")
                else:
                    self.dropCircle(self.gameBoard, row, col, 2)
                    if self.winningMove(self.gameBoard, 2):
                        self.draw_board()
                        self.gameOver = True
                        self.show_winner("YELLOW")

                self.draw_board()
                self.turn += 1
                self.turn = self.turn % 2

    def show_winner(self, player):
        winner = f"PLAYER {player} WON!"
        if messagebox.askyesno("Game Over", f"{winner}\nDo you want to play again?"):
            self.reset_game()
        else:
            self.root.quit()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4(root)
    root.mainloop()
