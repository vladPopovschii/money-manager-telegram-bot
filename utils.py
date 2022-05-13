from datetime import datetime


def calc_totals(payments: list) -> dict:
    total_map = {}

    for payment in payments:
        if total_map.get(payment["user_id"]) == None:
            total_map[payment["user_id"]] = 0

        total_map[payment["user_id"]
                  ] = total_map[payment["user_id"]] + payment["amount"]

    return total_map


def populate_username(payments: dict, users: list) -> dict:
    populated = {}

    for user_id in payments:
        for user in users:
            if user['user_id'] == user_id:
                populated[user_id] = {
                    "fullname": user["fullname"],
                    "amount": payments[user_id]
                }

    return populated


def generate_markup(populated_map: dict) -> str:
    markup = ""

    for user_id in populated_map:
        markup = markup + '<b>' + \
            populated_map[user_id]["fullname"] + '</b>: ' + \
            str(populated_map[user_id]["amount"]) + '\n'

    return markup


format_data = "%d/%m/%y %H:%M:%S"


def generate_history_markup(payments: list, users: list):
    markup = ""

    for payment in payments:
        user_fullname = find_fullname(users, payment["user_id"])
        markup = markup + '<b>' + user_fullname + '</b>: ' + \
            str(payment["amount"]) + ' (<i>' + str(payment["created_at"]
                                                   ) + "  " + payment["description"] + ')</i>\n'

    return markup


def find_fullname(users: list, user_id: int) -> str:
    for user in users:
        if user["user_id"] == user_id:
            return user["fullname"]

    return "Unknown user"


def generate_loans(populated_map: dict) -> str:

    max_amount = find_max(populated_map)

    user_debts = {}

    loan_string = ""

    for user_id in populated_map:
        if populated_map[user_id]['amount'] != max_amount:
            user_debts[user_id] = {
                "fullname": populated_map[user_id]["fullname"],
                "debt": (max_amount - populated_map[user_id]["amount"]) / len(populated_map)
            }

    print(user_debts)

    for user_id in user_debts:
        loan_string = loan_string + '<b>' + \
            user_debts[user_id]["fullname"] + "</b> has to pay: " + \
            str(user_debts[user_id]["debt"]) + "\n"

    return loan_string


def find_max(populated_map: dict) -> float:
    max_amount = None
    for user_id in populated_map:
        if(max_amount == None):

            max_amount = populated_map[user_id]["amount"]
        if max_amount < populated_map[user_id]["amount"]:
            max_amount = populated_map[user_id]["amount"]

    return max_amount
