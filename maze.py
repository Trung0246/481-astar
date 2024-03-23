# Trung, Michael

import numpy as np
import string
from collections import deque
from typing import List, Tuple

# Function to generate a 10x10 grid of random letters
def generate_grid(size: int = 10) -> np.ndarray:
	return np.random.choice(list(string.ascii_lowercase), size=(size, size))

# Check if all letters needed for the word are in the grid
def can_form_word(grid: np.ndarray, word: str) -> bool:
	grid_letters = ''.join(grid.flatten())
	for letter in word:
		if letter not in grid_letters:
			return False
	return True

# BFS implementation for horizontal and vertical movements
def bfs_adjusted(grid: np.ndarray, word: str) -> List[Tuple[int, int]]:
	if not can_form_word(grid, word):
		return [] # If any letter is missing, the word can't be formed
	
	rows, cols = grid.shape
	directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Only horizontal and vertical
	
	def get_neighbors(r: int, c: int):
		for dr, dc in directions:
			nr, nc = r + dr, c + dc
			if 0 <= nr < rows and 0 <= nc < cols:
				yield (nr, nc)

	def search_path(start: Tuple[int, int], target_char: str) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
		visited = set()
		queue = deque([(start, [])])
		while queue:
			(r, c), path = queue.popleft()
			if (r, c) in visited:
				continue
			visited.add((r, c))
			new_path = path + [(r, c)]
			if grid[r, c] == target_char:
				return (r, c), new_path
			for neighbor in get_neighbors(r, c):
				if neighbor not in visited:
					queue.append((neighbor, new_path))
		return start, []
	
	starts = list(zip(*np.where(grid == word[0])))
	shortest_path = None
	for start in starts:
		current_position = start
		path = [start]
		for char in word[1:]:
			current_position, partial_path = search_path(current_position, char)
			path.extend(partial_path[1:])  # Exclude the first element to avoid duplication
		if not shortest_path or (len(path) < len(shortest_path)):
			shortest_path = path
			
	return shortest_path if shortest_path else []

def print_path(grid: np.ndarray, path: List[Tuple[int, int]], word: str):
	path_set = set(path)
	word_chars = set(word)
	path_word_indices = {pos: word.index(grid[pos]) for pos in path if grid[pos] in word_chars}
	
	for step_index, (r, c) in enumerate(path):
		grid_copy = np.array([[char.lower() for char in row] for row in grid])  # Lowercase all letters
		current_char = grid[r][c].upper()
		print(f"Step {step_index + 1} - Move to '\033[95m{current_char}\033[0m':\n")

		for row_index, row in enumerate(grid_copy):
			row_str = " ".join(
				f"\033[95m{char.upper()}\033[0m" if (row_index, col_index) == (r, c) else
				(
					f"\033[92m{char.upper()}\033[0m"
						if (row_index, col_index) in path_set and
							(row_index, col_index) in path_word_indices.keys() and
							step_index >= path_word_indices[(row_index, col_index)]
						else (
							f"\033[93m{char.upper()}\033[0m"
							if (row_index, col_index) in path[:step_index]
							else char
						)
				)
				for col_index, char in enumerate(row)
			)
			print(row_str)
		print("\n---\n")

# Example usage
grid = generate_grid()
word = "womp"
path_adjusted = bfs_adjusted(grid, word)

if path_adjusted:
	print_path(grid, path_adjusted, word)
else:
	print("The word cannot be formed from the grid.")
