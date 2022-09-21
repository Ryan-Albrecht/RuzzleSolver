from collections import deque

with open("dictionary.txt") as f:
    words = set(f.read().splitlines())

starts_with_lookup = []

for l in range(2, 17):
    starts_with_lookup.append(set([word[:l] for word in words if len(word) >= l]))

class State:
    def __init__(self, board, head, parent) -> None:
        self.board = board
        self.head = head
        self.parent = parent
    
    def getWord(self):
        r,c = self.head
        currLetter = board[r][c]
        if self.parent is None:
            return currLetter
        return self.parent.getWord() + currLetter

# get board 
# format is each row separated by space
board = input("input: ").upper().split()

q = deque()

for row_i in range(4):
    for col_i in range(4):
        matrix = [[False]*4 for i in range(4)]
        matrix[row_i][col_i] = True
        s = State(matrix, (row_i, col_i), None)
        q.append(s)

found = set()

while q:
    c = q.popleft()
    cw = c.getWord()
    if len(cw) < 2 or cw in starts_with_lookup[len(cw) - 2]:
        if cw in words:
            found.add(cw)
        # add deltas from curr pos
        deltas = [(1, 0), (1,1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            
        for delta_row, delta_col in deltas:
            row, col = c.head
            row += delta_row
            col += delta_col
            # check if valid pos (within bounds)
            if 0 <= row <= 3 and 0 <= col <= 3 and not c.board[row][col]:
                # update matrix
                matrix = [row[:] for row in c.board]
                matrix[row][col] = True
                q.append(State(matrix, (row, col), c))

print(sorted(found, key=len))