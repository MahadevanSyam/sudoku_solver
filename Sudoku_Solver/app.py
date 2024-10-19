from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Check if placing `num` in board[row][col] is valid
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

# Cross-hatching logic
def cross_hatch(board):
    changed = True
    while changed:
        changed = False
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    possible_values = []
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            possible_values.append(num)
                    if len(possible_values) == 1:
                        board[row][col] = possible_values[0]
                        changed = True
    return board

# Backtracking logic
def solve_with_backtracking(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_with_backtracking(board):
                            return True
                        board[row][col] = 0  # Backtrack
                return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json['board']
    board = cross_hatch(data)
    if not solve_with_backtracking(board):
        return jsonify({'status': 'error', 'message': 'No solution exists.'})
    return jsonify({'status': 'success', 'board': board})

if __name__ == "__main__":
    app.run(debug=True)
