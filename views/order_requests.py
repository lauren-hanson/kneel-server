import sqlite3
import json
from models import Orders, Metals, Styles, Sizes
from .size_requests import get_single_size
from .metal_requests import get_single_metal
from .style_requests import get_single_style

ORDERS = [

]


def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.style_id,
            o.size_id, 
            m.metal metal_metal, 
            m.price metal_price, 
            z.carets size_carets, 
            z.price size_price,
            s.style style_style, 
            s.price style_price
        FROM Orders o
        JOIN Metals m 
            ON m.id = o.metal_id
        JOIN Sizes z 
            ON z.id = o.size_id
        JOIN Styles s 
            ON s.id = o.style_id
        """)

        orders = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            # Create an order instance from the current row
            order = Orders(row['id'], row['metal_id'],
                           row['style_id'], row['size_id'])
            metal = Metals(row['id'], row['metal_metal'], row['metal_price'])
            size = Sizes(row['id'], row['size_carets'], row['size_price'])
            style = Styles(row['id'], row['style_style'], row['style_price'])

            order.metal = metal.__dict__
            order.size = size.__dict__
            order.style = style.__dict__

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


def delete_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM orders
        WHERE id = ?
        """, (id, ))


def update_order(id, new_order):
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break
