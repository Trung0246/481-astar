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
	# Check if all letters needed for the word are present in the grid
	# Time Complexity: O(n*m), where n and m are the dimensions of the grid
	# Space Complexity: O(1), just for the iteration, no extra storage
	if not can_form_word(grid, word):
		return []  # If any letter is missing, the word can't be formed
	
	rows, cols = grid.shape  # Get the number of rows and columns in the grid
	# Directions represent the four possible movements: up, down, left, right
	directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
	
	# Function to get all valid neighboring positions for a given cell
	# This helps in finding adjacent cells to explore in the BFS
	def get_neighbors(r: int, c: int):
		for dr, dc in directions:
			nr, nc = r + dr, c + dc
			# Check if the new position is within the grid boundaries
			if 0 <= nr < rows and 0 <= nc < cols:
				yield (nr, nc)  # Return the valid neighbor position
	
	# Function to search for the next character in the word using BFS
	# This function tries to find a path to the target character in the grid
	def search_path(start: Tuple[int, int], target_char: str) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
		visited = set()  # To keep track of already visited cells
		queue = deque([(start, [])])  # Initialize the queue with the start position and empty path
		
		# Continue the search until there are no cells left to explore
		while queue:
			(r, c), path = queue.popleft()  # Get the next cell and the path to it
			if (r, c) in visited:  # Skip if this cell has already been visited
				continue
			visited.add((r, c))  # Mark the current cell as visited
			
			new_path = path + [(r, c)]  # Add the current cell to the path
			# Check if the current cell contains the target character
			if grid[r, c] == target_char:
				return (r, c), new_path  # Return the current position and path
			
			# Explore all valid neighbors of the current cell
			for neighbor in get_neighbors(r, c):
				if neighbor not in visited:
					queue.append((neighbor, new_path))  # Add to queue for future exploration
		
		# If the target character is not found, return the start position and empty path
		return start, []
	
	# Find all positions in the grid that match the first character of the word
	starts = list(zip(*np.where(grid == word[0])))
	shortest_path = None  # Initialize the shortest path variable
	
	# Try to form the word starting from each found starting position
	for start in starts:
		current_position = start
		path = [start]
		# Iterate over each character in the word (after the first one)
		for char in word[1:]:
			# Search for the next character in the word
			current_position, partial_path = search_path(current_position, char)
			path.extend(partial_path[1:])  # Append the found path excluding the starting position to avoid duplication
		
		# Update the shortest path if a shorter one is found
		if not shortest_path or (len(path) < len(shortest_path)):
			shortest_path = path
	
	# Return the shortest path found, or an empty list if none is found
	return shortest_path if shortest_path else []

# Time Complexity of bfs_adjusted: O(n*m*k), where k is the length of the word.
# This is due to potentially scanning the entire grid for each character in the word.
# Space Complexity: O(n*m) primarily due to the storage of the grid and the queue used in BFS.

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
word = "thin"
path_adjusted = bfs_adjusted(grid, word)

if path_adjusted:
	print_path(grid, path_adjusted, word)
else:
	print("The word cannot be formed from the grid.")
