# Group C
# Lau Kai Yeung 21214638​
# Le Ching Wa, Louis 22205276​
# Lee Wang, Ryan 20236700​
# Lau Shing Yuk 20203810​
# Tung Lok Yin, Jason 20203802​
# Chan Chi Hin, Jonathan 20202288

import json


def name_address(customer_number):
    # Access the customer data
    open_file = open('customer.json')
    customer_detail = json.load(open_file)
    customer_number=str(customer_number)

    # Return the customer detail by customer number, return a message if not found
    if customer_number in customer_detail:
        return customer_detail[customer_number]["customer_name"], customer_detail[customer_number]["customer_address"], customer_detail[customer_number]["invoice_date"]
    else:
        return "Customer not found", "Customer not found"



