import tkinter as tk
from tkinter import messagebox
import random

SNAKES = {99: 54, 70: 55, 52: 42, 25: 2, 95: 72}
LADDERS = {6: 25, 11: 40, 60: 85, 46: 90, 17: 69}

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        root.title("Snake & Ladder")
        root.geometry("760x650")
        root.configure(bg="#f4f0ff")
        self.positions = [0, 0]
        self.turn = 0
        self.colors = ["#e85d75", "#2878b5"]

        tk.Label(root, text="🐍 Snake & Ladder 🪜", font=("Arial", 22, "bold"),
                 bg="#f4f0ff", fg="#483d8b").pack(pady=10)
        self.status = tk.Label(root, text="Player 1's turn", font=("Arial", 14, "bold"),
                               bg="#f4f0ff")
        self.status.pack()
        self.board = tk.Canvas(root, width=600, height=500, bg="white",
                               highlightthickness=1, highlightbackground="#aaa")
        self.board.pack(pady=10)
        controls = tk.Frame(root, bg="#f4f0ff")
        controls.pack()
        self.roll_button = tk.Button(controls, text="Roll Dice 🎲", command=self.roll,
                                     font=("Arial", 12, "bold"), bg="#8b78d1",
                                     fg="white", padx=18, pady=8)
        self.roll_button.pack(side="left", padx=8)
        tk.Button(controls, text="New Game", command=self.reset, font=("Arial", 12),
                  padx=15, pady=8).pack(side="left", padx=8)
        self.dice_label = tk.Label(root, text="Roll the dice to begin!", bg="#f4f0ff",
                                   font=("Arial", 12))
        self.dice_label.pack(pady=8)
        self.draw_board()

    def cell_center(self, number):
        n = number - 1
        row_from_bottom, col_in_row = divmod(n, 10)
        col = col_in_row if row_from_bottom % 2 == 0 else 9 - col_in_row
        row = 9 - row_from_bottom
        return col * 60 + 30, row * 50 + 25

    def draw_board(self):
        self.board.delete("all")
        for number in range(1, 101):
            x, y = self.cell_center(number)
            col, row = int(x // 60), int(y // 50)
            fill = "#f8f4ff" if (row + col) % 2 == 0 else "#e9e2fb"
            self.board.create_rectangle(col*60, row*50, (col+1)*60, (row+1)*50,
                                        fill=fill, outline="#c9c0df")
            self.board.create_text(x, y-8, text=str(number), font=("Arial", 8),
                                   fill="#51466f")
        for start, end in LADDERS.items():
            x1, y1 = self.cell_center(start)
            x2, y2 = self.cell_center(end)
            self.board.create_line(x1, y1, x2, y2, fill="#269b65", width=5)
            self.board.create_text((x1+x2)/2, (y1+y2)/2, text="L",
                                   fill="#12613c", font=("Arial", 12, "bold"))
        for start, end in SNAKES.items():
            x1, y1 = self.cell_center(start)
            x2, y2 = self.cell_center(end)
            self.board.create_line(x1, y1, x2, y2, fill="#d94d59", width=5,
                                   smooth=True)
            self.board.create_text((x1+x2)/2, (y1+y2)/2, text="S",
                                   fill="#9e2632", font=("Arial", 12, "bold"))
        for i, pos in enumerate(self.positions):
            if pos:
                x, y = self.cell_center(pos)
                offset = -10 if i == 0 else 10
                self.board.create_oval(x-9+offset, y+5, x+9+offset, y+23,
                                       fill=self.colors[i], outline="white", width=2)
        self.board.create_text(8, 8, anchor="nw", text="Green = ladder   Red = snake",
                               font=("Arial", 9, "bold"), fill="#51466f")

    def roll(self):
        dice = random.randint(1, 6)
        old = self.positions[self.turn]
        new = old + dice
        message = f"Player {self.turn+1} rolled {dice}. "
        if new > 100:
            message += "You need an exact roll to reach 100."
        else:
            if new in LADDERS:
                message += f"Ladder! Climb from {new} to {LADDERS[new]}."
                new = LADDERS[new]
            elif new in SNAKES:
                message += f"Snake! Slide from {new} to {SNAKES[new]}."
                new = SNAKES[new]
            self.positions[self.turn] = new
        self.dice_label.config(text=message)
        self.draw_board()
        if self.positions[self.turn] == 100:
            messagebox.showinfo("Winner!", f"Player {self.turn+1} wins!")
            self.roll_button.config(state="disabled")
            self.status.config(text=f"Player {self.turn+1} wins!")
            return
        self.turn = 1 - self.turn
        self.status.config(text=f"Player {self.turn+1}'s turn")

    def reset(self):
        self.positions = [0, 0]
        self.turn = 0
        self.roll_button.config(state="normal")
        self.status.config(text="Player 1's turn")
        self.dice_label.config(text="New game started. Roll the dice!")
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    SnakeLadderGame(root)
    root.mainloop()
