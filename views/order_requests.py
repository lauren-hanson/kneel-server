import sqlite3
import json
from models import Orders
from .size_requests import get_single_size
from .metal_requests import get_single_metal
from .style_requests import get_single_style

ORDERS = [
    {
        "id": 1,
        "metal_id": "",
        "size_id": "",
        "style_id": "",
    }
]


def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.metal_id, 
            a.size_id, 
            a.style_id
        FROM Orders a 
        """)

        orders = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            order = Orders(row['id'], row['metal_id'],
                           row['size_id'], row['style_id'])

            orders.append(order.__dict__)
    return orders


def get_single_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT 
            a.id, 
            a.metal_id, 
            a.size_id, 
            a.style_id
        FROM Orders a 
        WHERE a.id = ?
        """, (id, ))
        # Load the single result into memory
        data = db_cursor.fetchone()
        # Create an order instance from the current row
        order = Orders(data['id'], data['metal_id'], data['size_id'],
                       data['style_id'])

        return order.__dict__


def create_order(new_order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Orders
            (metal_id, size_id, style_id)
        VALUES
            (?, ?, ?); 
        """, (new_order['metal_id'], new_order['size_id'], new_order['style_id']))

        id = db_cursor.lastrowid
        new_order['id'] = id 
    return new_order


# def create_order(order):
#     # Get the id value of the last order in the list
#     max_id = ORDERS[-1]["id"]
#     # Add 1 to whatever that number is
#     new_id = max_id + 1
#     # Add an `id` property to the order dictionary
#     order["id"] = new_id
#     # Add the order dictionary to the list
#     ORDERS.append(order)
#     # Return the dictionary with `id` property added
#     return order


def delete_order(id):
    # Initial -1 value for order index, in case one isn't found
    order_index = -1

    # Iterate the ORDERS list, but use enumerate() so that you
    # can access the index value of each item
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Store the current index.
            order_index = index

    # If the order was found, use pop(int) to remove it from list
    if order_index >= 0:
        ORDERS.pop(order_index)


def update_order(id, new_order):
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break
