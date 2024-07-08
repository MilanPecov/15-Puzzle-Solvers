import tkinter as tk
import threading
from fifteen_puzzle_solvers.services.algorithms import AStar
from fifteen_puzzle_solvers.services.solver import PuzzleSolver
from fifteen_puzzle_solvers.services.puzzle.shuffle import PuzzleShuffleService

class PuzzleGame:
    def __init__(self, master):
        self.master = master
        self.master.title('15 Puzzle Game')
        self.master.geometry('400x600')
        self.master.configure(bg='#2E2E2E')

        self.puzzle_size = 4
        self.puzzle = PuzzleShuffleService.shuffle_puzzle(self.puzzle_size)
        self.solution_steps = []
        self.current_step = 0
        self.num_expanded_nodes = 0

        self.tiles = []
        self.create_ui()

    def create_ui(self):
        self.title = tk.Label(self.master, text='15 Puzzle Game', font=('Helvetica', 20), fg='#FFFFFF', bg='#2E2E2E')
        self.title.pack(pady=10)

        self.puzzle_frame = tk.Frame(self.master, bg='#2E2E2E')
        self.puzzle_frame.pack(pady=20)

        self.create_tiles()

        self.shuffle_button = tk.Button(self.master, text='Shuffle', command=self.shuffle_puzzle, bg='#28A745',
                                        fg='white', width=10)
        self.shuffle_button.pack(pady=5)

        self.solve_button = tk.Button(self.master, text='Solve', command=self.start_solve_puzzle, bg='#FFC107',
                                      fg='black', width=10)
        self.solve_button.pack(pady=5)

        self.button_frame = tk.Frame(self.master, bg='#2E2E2E')
        self.button_frame.pack(pady=5)

        self.previous_button = tk.Button(self.button_frame, text='Previous Step', command=self.previous_step,
                                         bg='#007BFF', fg='white', width=15)
        self.previous_button.grid(row=0, column=0, padx=10)

        self.next_button = tk.Button(self.button_frame, text='Next Step', command=self.next_step, bg='#007BFF',
                                     fg='white', width=15)
        self.next_button.grid(row=0, column=1, padx=10)

        self.previous_button.grid_remove()
        self.next_button.grid_remove()

        self.status_label = tk.Label(self.master, text='Moves: 0\nExpanded Nodes: 0\nSolution Steps: 0',
                                     font=('Helvetica', 12), fg='#FFFFFF', bg='#2E2E2E')
        self.status_label.pack(pady=10)

    def create_tile_button(self, i, j):
        return tk.Button(self.puzzle_frame, text=str(self.puzzle.position[i][j]), font=('Helvetica', 18), width=4,
                         height=2, bg='#007BFF', fg='white', command=lambda: self.move_tile(i, j))

    def create_tiles(self):
        for i in range(self.puzzle_size):
            row = []
            for j in range(self.puzzle_size):
                tile = self.create_tile_button(i, j)
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)
        self.update_tiles()

    def update_tiles(self):
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                text = str(self.puzzle.position[i][j])
                if text == '0':
                    text = ''
                self.tiles[i][j].config(text=text)

    def update_status_label(self):
        text = (f'Moves: {self.current_step}\n'
                f'Expanded Nodes: {self.num_expanded_nodes}\n'
                f'Solution Steps: {len(self.solution_steps)}')
        self.status_label.config(text=text)

    def move_tile(self, i, j):
        empty_i, empty_j = self.puzzle.find_empty_tile()
        if (abs(empty_i - i) == 1 and empty_j == j) or (abs(empty_j - j) == 1 and empty_i == i):
            self.puzzle.position = self.puzzle.swap_tiles(i, j, empty_i, empty_j)
            self.update_tiles()
            self.current_step += 1
            self.update_status_label()

    def shuffle_puzzle(self):
        self.puzzle = PuzzleShuffleService.shuffle_puzzle(self.puzzle_size)
        self.solution_steps = []
        self.current_step = 0
        self.update_tiles()
        self.update_status_label()
        self.previous_button.grid_remove()
        self.next_button.grid_remove()
        self.solve_button.pack(pady=5)  # Show the solve button again

    def start_solve_puzzle(self):
        self.solve_button.config(text='Solving...', state=tk.DISABLED)
        self.status_label.config(text='Solving...')
        threading.Thread(target=self.solve_puzzle).start()

    def solve_puzzle(self):
        solver = PuzzleSolver(AStar(self.puzzle, heuristic='total'))
        solver.run()
        self.solution_steps = solver.get_solution()
        self.num_expanded_nodes = solver.get_num_expanded_nodes()
        self.current_step = 0
        self.master.after(0, self.on_solve_complete)

    def on_solve_complete(self):
        self.update_tiles()
        self.update_status_label()
        self.solve_button.config(text='Solve', state=tk.NORMAL)
        self.solve_button.pack_forget()  # Hide the solve button
        self.previous_button.grid()
        self.next_button.grid()

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.puzzle = self.solution_steps[self.current_step]
            self.update_tiles()
            self.update_status_label()

    def next_step(self):
        if self.current_step < len(self.solution_steps) - 1:
            self.current_step += 1
            self.puzzle = self.solution_steps[self.current_step]
            self.update_tiles()
            self.update_status_label()
