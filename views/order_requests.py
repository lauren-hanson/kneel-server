ORDERS = [
    {
        "id": 1,
        "metalId": 1,
        "sizeId": 2,
        "styleId": 3
    }
]


def get_all_orders():
    return ORDERS

# Function with a single parameter
def get_single_order(id):
    # Variable to hold the found order, if it exists
    requested_order = None

    # Iterate the ORDERS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for order in ORDERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if order["id"] == id:
            requested_order = order

    return requested_order
