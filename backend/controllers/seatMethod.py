from models.model import Seat

NUM_ROWS = 10
NUM_COLUMNS = 10

def initialize_seat_matrix():
    return [[0 for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]


def update_seat_status(row, column, status):
    # Update the seat status in the database
    Seat.update_one(
        {"row": row},
        {"$set": {f"seats.{column}": status}}
    )