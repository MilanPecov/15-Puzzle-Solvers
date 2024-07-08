from fifteen_puzzle_solvers.ui.puzzle_game import PuzzleGame

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    game = PuzzleGame(root)
    root.mainloop()
