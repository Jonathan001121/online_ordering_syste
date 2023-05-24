# Group C
# Lau Kai Yeung 21214638​
# Le Ching Wa, Louis 22205276​
# Lee Wang, Ryan 20236700​
# Lau Shing Yuk 20203810​
# Tung Lok Yin, Jason 20203802​
# Chan Chi Hin, Jonathan 20202288

import pandas as pd
import json


# Convert the CSV file to JSON
def convert_order_csv_to_json():

    # Prompt user to enter filename
    filename = input("Enter filename (including extension .csv): ")
    while not filename.endswith('.csv'):
        filename = input("Enter filename (including extension .csv): ")
    df = pd.read_csv(filename)

    # Sort the DataFrame by staff_number and customer_number
    df = df.sort_values(by=['order'])

    # get the order max number
    order_max = str(df['order'].max())
    
    if order_max >"9":
        print("Error: Maximum number of orders exceeded (Maximum <= 9).")
        return

    # Group the orders by staff_number and customer_number
    orders_grouped = df.groupby(['order','staff_number', 'customer_number',])

    # Create a list to hold the final JSON data
    json_data = {'number_of_orders': order_max, 'orders': []}

    # Loop through each order group
    for i, group in enumerate(orders_grouped):

        order_number,staff_number, customer_number= group[0]
        items = []

        for index, row in group[1].iterrows():
            item = {'item_number': row['item_number'], 'item_name': row['item_name'],
                    'quantity': row['quantity'], 'cost': row['cost']}
            items.append(item)

        discounts = {'VIP': row['discounts_VIP'], 'VIPDay95': row['discounts_VIPDay95'], 'VIPDay123': row['discounts_VIPDay123']}

        # Create the order dictionary
        order = {'staff_number': str(staff_number), 'items': items, 'discounts': discounts,
                'customer_number': str(customer_number)}

        # Append the order dictionary to the orders list
        json_data['orders'].append(order)



    # Convert the JSON data to a string
    json_string = json.dumps(json_data, indent=4)

    # Write the JSON string to a file
    with open('input.json', 'w') as f:
        f.write(json_string)
