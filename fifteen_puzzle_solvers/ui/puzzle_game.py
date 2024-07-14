import tkinter as tk
import threading
from fifteen_puzzle_solvers.services.algorithms import AStar, BreadthFirst
from fifteen_puzzle_solvers.services.solver import PuzzleSolver
from fifteen_puzzle_solvers.services.puzzle.shuffle import PuzzleShuffleService
from fifteen_puzzle_solvers.services.puzzle.constants import (
    HEURISTIC_OPTIONS, HEURISTIC_TOTAL, ALGORITHM_OPTIONS, ASTAR)


class PuzzleGame:
    def __init__(self, master):
        self.master = master
        self.master.title('15 Puzzle Game')
        self.master.geometry('600x860')
        self.master.configure(bg='#2E2E2E')

        self.puzzle_size = 4
        self.puzzle = PuzzleShuffleService.shuffle_puzzle(self.puzzle_size)
        self.solution_steps = []
        self.current_step = 0
        self.num_expanded_nodes = 0
        self.solver = None

        self.tiles = []
        self.selected_algorithm = tk.StringVar(self.master, ASTAR)
        self.selected_heuristic = tk.StringVar(self.master, HEURISTIC_TOTAL)
        self.selected_size = tk.IntVar(self.master, self.puzzle_size)
        self.create_ui()

    def create_ui(self):
        self.title = tk.Label(self.master, text='15 Puzzle Game', font=('Helvetica', 20), fg='#FFFFFF', bg='#2E2E2E')
        self.title.pack(pady=10)

        self.size_label = tk.Label(self.master, text='Select Size:', font=('Helvetica', 12), fg='#FFFFFF', bg='#2E2E2E')
        self.size_label.pack(pady=5)

        self.size_menu = tk.OptionMenu(self.master, self.selected_size, *range(3, 11), command=self.on_size_change)
        self.size_menu.pack(pady=5)

        self.shuffle_button = tk.Button(self.master, text='Shuffle', command=self.shuffle_puzzle, bg='#28A745',
                                        fg='white', width=10)
        self.shuffle_button.pack(pady=5)

        self.puzzle_frame = tk.Frame(self.master, bg='#2E2E2E')
        self.puzzle_frame.pack(pady=20)

        self.controls_frame = tk.Frame(self.master, bg='#2E2E2E')
        self.controls_frame.pack(pady=10)

        self.algorithm_label = tk.Label(self.controls_frame, text='Select Algorithm:', font=('Helvetica', 12),
                                        fg='#FFFFFF', bg='#2E2E2E')
        self.algorithm_label.grid(row=0, column=0, pady=5, padx=5, sticky='e')

        self.algorithm_menu = tk.OptionMenu(self.controls_frame, self.selected_algorithm, *ALGORITHM_OPTIONS,
                                            command=self.on_algorithm_change)
        self.algorithm_menu.grid(row=0, column=1, pady=5, padx=5)

        self.heuristic_label = tk.Label(self.controls_frame, text='Select Heuristic:', font=('Helvetica', 12),
                                        fg='#FFFFFF', bg='#2E2E2E')
        self.heuristic_label.grid(row=1, column=0, pady=5, padx=5, sticky='e')

        self.heuristic_menu = tk.OptionMenu(self.controls_frame, self.selected_heuristic, *HEURISTIC_OPTIONS)
        self.heuristic_menu.grid(row=1, column=1, pady=5, padx=5)

        self.solve_button = tk.Button(self.controls_frame, text='Solve', command=self.start_solve_puzzle, bg='#FFC107',
                                      fg='black', width=10)
        self.solve_button.grid(row=2, column=0, pady=10, padx=5, columnspan=2)

        self.stop_button = tk.Button(self.controls_frame, text='Stop', command=self.stop_solve_puzzle, bg='#DC3545',
                                     fg='white', width=10)
        self.stop_button.grid(row=3, column=0, pady=5, padx=5, columnspan=2)
        self.stop_button.grid_remove()  # Hide the stop button initially

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

        self.create_tiles()

    def on_algorithm_change(self, value):
        if value == 'A*':
            self.heuristic_label.grid()
            self.heuristic_menu.grid()
        else:
            self.heuristic_label.grid_remove()
            self.heuristic_menu.grid_remove()

    def on_size_change(self, value):
        self.puzzle_size = value
        self.puzzle = PuzzleShuffleService.shuffle_puzzle(self.puzzle_size)
        self.create_tiles()
        self.update_tiles()

    def create_tile_button(self, i, j):
        return tk.Button(self.puzzle_frame, text=str(self.puzzle.position[i][j]), font=('Helvetica', 18), width=4,
                         height=2, bg='#007BFF', fg='white', command=lambda: self.move_tile(i, j))

    def create_tiles(self):
        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()
        self.tiles = []
        for i in range(self.puzzle_size):
            row = []
            for j in range(self.puzzle_size):
                tile = self.create_tile_button(i, j)
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

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
        self.num_expanded_nodes = 0
        self.update_tiles()
        self.update_status_label()
        self.previous_button.grid_remove()
        self.next_button.grid_remove()
        self.solve_button.grid()  # Show the solve button again

    def start_solve_puzzle(self):
        self.solve_button.grid_remove()  # Hide the solve button
        self.stop_button.grid()  # Show the stop button
        self.solve_button.config(text='Solving...', state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text='Solving...')
        threading.Thread(target=self.solve_puzzle).start()

    def stop_solve_puzzle(self):
        if self.solver:
            self.solver.stop()
            self.solve_button.config(text='Solve', state=tk.NORMAL)
            self.stop_button.grid_remove()  # Hide the stop button
            self.solve_button.grid()  # Show the solve button
            self.status_label.config(text='Stopped')

    def solve_puzzle(self):
        selected_algorithm = self.selected_algorithm.get()
        if selected_algorithm == 'A*':
            selected_heuristic = self.selected_heuristic.get() or HEURISTIC_TOTAL
            self.solver = PuzzleSolver(AStar(self.puzzle, heuristic=selected_heuristic))
        else:
            self.solver = PuzzleSolver(BreadthFirst(self.puzzle))

        self.solver.run()
        self.solution_steps = self.solver.get_solution()
        self.num_expanded_nodes = self.solver.get_num_expanded_nodes()
        self.current_step = 0
        self.master.after(0, self.on_solve_complete)

    def on_solve_complete(self):
        self.update_tiles()
        self.update_status_label()
        self.solve_button.grid()  # Show the solve button
        self.solve_button.config(text='Solve', state=tk.NORMAL)
        self.stop_button.grid_remove()  # Hide the stop button
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
