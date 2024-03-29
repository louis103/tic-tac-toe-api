from flask import Flask, request, jsonify

app = Flask(__name__)


def is_valid_board(board):
    # Check if the board is valid
    if len(board) != 9:
        return False
    if not all(char in "ox " for char in board):
        return False
    x_count = board.count("x")
    o_count = board.count("o")
    if abs(x_count - o_count) > 1:
        return False
    return True


def get_best_move(board):
    # First we Implement the optimal play algorithm for Tic-Tac-Toe
    # Returns the board with 'o' placed in the best move position
    # For simplicity, we'll implement the strategy directly in this function
    # without breaking down into separate functions for each step

    # Win: Check for immediate win
    for i in range(0, 9, 3):
        if board[i : i + 3].count("o") == 2 and " " in board[i : i + 3]:
            return (
                board[: i + board[i : i + 3].index(" ")]
                + "o"
                + board[i + board[i : i + 3].index(" ") + 1 :]
            )

    for i in range(3):
        if board[i::3].count("o") == 2 and " " in board[i::3]:
            index = i + (3 * board[i::3].index(" "))
            return board[:index] + "o" + board[index + 1 :]

    if board[0] == board[4] == "o" and board[8] == " ":
        return board[:8] + "o" + board[9:]
    if board[2] == board[4] == "o" and board[6] == " ":
        return board[:6] + "o" + board[7:]

    # Block: Check for opponent's win and block
    for i in range(0, 9, 3):
        if board[i : i + 3].count("x") == 2 and " " in board[i : i + 3]:
            return (
                board[: i + board[i : i + 3].index(" ")]
                + "o"
                + board[i + board[i : i + 3].index(" ") + 1 :]
            )

    for i in range(3):
        if board[i::3].count("x") == 2 and " " in board[i::3]:
            index = i + (3 * board[i::3].index(" "))
            return board[:index] + "o" + board[index + 1 :]

    if board[0] == board[4] == "x" and board[8] == " ":
        return board[:8] + "o" + board[9:]
    if board[2] == board[4] == "x" and board[6] == " ":
        return board[:6] + "o" + board[7:]

    # Center: Occupy center if available
    if board[4] == " ":
        return board[:4] + "o" + board[5:]

    # Opposite corner: Occupy opposite corner if opponent is in the corner
    if board[0] == "x" and board[8] == " ":
        return board[:8] + "o" + board[9:]
    if board[2] == "x" and board[6] == " ":
        return board[:6] + "o" + board[7:]
    if board[6] == "x" and board[2] == " ":
        return board[:2] + "o" + board[3:]
    if board[8] == "x" and board[0] == " ":
        return board[:0] + "o" + board[1:]

    # Empty corner: Occupy empty corner
    for i in [0, 2, 6, 8]:
        if board[i] == " ":
            return board[:i] + "o" + board[i + 1 :]

    # Empty side: Occupy empty side
    for i in [1, 3, 5, 7]:
        if board[i] == " ":
            return board[:i] + "o" + board[i + 1 :]

    # If no move is possible (unlikely to reach here in Tic-Tac-Toe)
    return board


@app.route("/", methods=["GET"])
def tic_tac_toe():
    board = request.args.get("board", "")
    if not is_valid_board(board):
        return "Invalid board", 400

    if board.count("o") != board.count("x"):
        return "It's not O's turn", 400

    best_move = get_best_move(board)
    return best_move


@app.errorhandler(404)
def url_not_found(e):
    return (
        jsonify(
            {
                "status": 404,
                "message": "That URL is Not Found on our tic-tac-toe server",
            }
        ),
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
