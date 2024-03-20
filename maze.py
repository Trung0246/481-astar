# Trung, Michael

import time
import random

import networkx # For bfs, dfs, a*

maze_size = [15, 15]
maze_data = []
word_data = set()

for i in range(maze_size[0] * maze_size[1]):
	maze_data.append("")

# Load dictionary
with open("word.txt", "r") as file:
	for line in file:
		word_data.add(line.strip())

while True:
	# Intialize maze
	maze_data.clear()

	# Randomly put blocker (indicated by "@")
	for i in range(maze_size[0] * maze_size[1]):
		# Avoid bottom center and top center
		if i == maze_size[0] * maze_size[1] // 2 or i == maze_size[0] * maze_size[1] // 2 - maze_size[1]:
			maze_data.append(" ")
			continue
		maze_data.append("@" if random.random() < 0.1 else " ")

	# Put starting point at bottom center
	maze_data[maze_size[0] * maze_size[1] // 2] = "~"

	# Put ending point at top center
	maze_data[maze_size[0] * maze_size[1] // 2 - maze_size[1]] = "#"

	while True:
		# Inline print then wait for user input
		word_curr = input("Enter word: ")

		if word_curr == "@":
			break

		# Check if word is in dictionary
		if word_curr not in word_data:
			print("Word not valid.")
			continue

		# Check if word would fit in the maze
		if len(word_curr) > maze_size[0] or len(word_curr) > maze_size[1]:
			print("Word too long.")
			continue

		# [TODO] Supposed to perform word fitting logic here?

		# Render maze
		for i in range(maze_size[0]):
			for j in range(maze_size[1]):
				print(maze_data[i * maze_size[1] + j], end=" ")
			print()
