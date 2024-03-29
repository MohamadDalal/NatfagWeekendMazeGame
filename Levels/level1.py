# This is a level script. It has a 27x16 list of lists with strings inside.
# Each string specifies the shape of a square in the maze, where 0 means no wall and 1 means there is a wall:
#   - The first number is the upper wall
#   - The second number is the right wall
#   - The third number is the bottom wall
#   - The fourth number is the right wall

levelList = [["0000", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "1101", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0010", "0000"],
             ["0100", "1011", "1010", "1000", "1100", "1001", "1110", "1001", "1010", "1100", "1001", "1100", "1001", "0010", "1000", "1110", "1001", "1100", "1001", "1010", "1010", "1010", "1100", "1011", "1100", "1101", "0001"],
             ["0100", "1001", "1100", "0101", "0101", "0011", "1010", "0110", "1001", "0010", "0110", "0111", "0011", "1100", "0011", "1100", "0101", "0101", "0011", "1010", "1010", "1100", "0011", "1010", "0110", "0101", "0001"],
             ["0100", "0101", "0011", "0110", "0011", "1010", "1100", "1011", "0100", "1001", "1100", "1001", "1010", "0010", "1100", "0011", "0110", "0001", "1010", "1010", "1010", "0110", "1011", "1010", "1100", "0101", "0001"],
             ["0100", "0101", "1001", "1010", "1110", "1001", "0000", "1010", "0010", "0110", "0111", "0101", "1011", "1010", "0010", "1110", "1001", "0110", "1001", "1100", "1101", "1001", "1010", "1100", "0001", "0110", "0001"],
             ["0100", "0101", "0101", "1101", "1001", "0100", "0101", "1001", "1100", "1001", "1100", "0111", "1001", "1100", "1001", "1000", "0000", "1010", "0110", "0101", "0001", "0110", "1101", "0101", "0011", "1100", "0001"],
             ["0100", "0001", "0110", "0001", "0110", "0111", "0101", "0111", "0101", "0101", "0101", "1001", "0110", "0011", "0110", "0101", "0011", "1010", "1100", "0011", "0110", "1101", "0101", "0001", "1100", "0101", "0001"],
             ["0100", "0011", "1100", "0101", "1001", "1100", "0101", "1001", "0110", "0101", "0001", "0110", "1001", "1010", "1100", "0111", "1001", "1100", "0001", "1100", "1011", "0100", "0101", "0101", "0011", "0110", "0001"],
             ["0100", "1101", "0101", "0101", "0101", "0101", "0011", "0110", "1001", "0110", "0111", "1001", "0110", "1101", "0011", "1100", "0101", "0101", "0111", "0101", "1001", "0010", "0100", "0101", "1001", "1100", "0001"],
             ["0100", "0001", "0110", "0011", "0110", "0011", "1010", "1000", "0110", "1001", "1000", "0010", "1110", "0101", "1001", "0110", "0101", "0101", "1001", "0100", "0011", "1100", "0011", "0110", "0101", "0101", "0001"],
             ["0100", "0101", "1101", "1001", "1010", "1010", "1100", "0101", "1001", "0100", "0011", "1110", "1001", "0010", "0100", "1001", "0110", "0011", "0110", "0101", "1101", "0011", "1010", "1010", "0110", "0101", "0001"],
             ["0100", "0101", "0101", "0011", "1100", "1001", "0110", "0101", "0101", "0101", "1001", "1100", "0011", "1110", "0101", "0101", "1101", "1001", "1100", "0101", "0011", "1000", "1010", "1010", "1100", "0101", "0001"],
             ["0100", "0101", "0011", "1010", "0110", "0011", "1100", "0111", "0101", "0111", "0101", "0011", "1010", "1100", "0011", "0110", "0001", "0110", "0101", "0011", "1100", "0011", "1010", "1100", "0101", "0101", "0001"],
             ["0100", "0101", "1001", "1010", "1010", "1100", "0101", "1001", "0110", "1001", "0100", "1101", "1001", "0110", "1001", "1010", "0110", "1101", "0011", "1100", "0011", "1100", "1101", "0101", "0111", "0101", "0001"],
             ["0100", "0011", "0110", "1011", "1010", "0010", "0110", "0011", "1010", "0110", "0011", "0110", "0011", "1100", "0011", "1010", "1010", "0110", "1011", "0010", "1010", "0110", "0011", "0010", "1010", "0110", "0001"],
             ["0000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "0111", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "1000", "0000"]]
# These two lists specify the position of the start and end squares
startPos = [13,15]
endPos = [13,0]