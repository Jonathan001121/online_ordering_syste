# Group C
# Lau Kai Yeung 21214638​
# Le Ching Wa, Louis 22205276​
# Lee Wang, Ryan 20236700​
# Lau Shing Yuk 20203810​
# Tung Lok Yin, Jason 20203802​
# Chan Chi Hin, Jonathan 20202288

import json
import pandas as pd
import determineNextOrderNumber as dNON
from convertorder import convert_order_csv_to_json

# open the text file in read mode
with open("lastInputNumber.txt", "r") as f:
    # read the contents of the file
    order_number = f.read()

# call the function to convert the CSV file to JSON
convert_order_csv_to_json()

#read the JSON data from the external file
with open("input.json", "r") as f:
    data = json.load(f)

# create a temporary list to store the split orders
split_orders = []

# iterate through each order in the JSON data
for order in data["orders"]:
    items_length = len(order["items"])
    # if the order has more than 9 items, split it into multiple orders with 9 items each
    if items_length > 9:
        num_splits = (items_length // 9) + (items_length % 9 > 0)  # calculate the number of splits
        for i in range(num_splits):
            # create a new order with 9 items and copy the order details
            new_order = dict(order)
            new_order["items"] = order["items"][i*9 : (i+1)*9]
            # new_order["order_number"] += f"-{i+1}"
            # add the new order to the temporary list
            split_orders.append(new_order)
    else:
        # add the original order to the temporary list
        split_orders.append(order)

# replace the original "orders" list with the split_orders list
data["orders"] = split_orders


# update the number_of_orders field in the JSON data object
data["number_of_orders"] = len(data["orders"])



for order in data["orders"]:
           order["order_number"]=dNON.get_next_order_number(order_number)
           order_number=order["order_number"]
# open a new file with write mode
with open("output_file.txt", "w") as f:
    # write the string to the file
    f.write(order_number)
# write the updated JSON data to the external file
with open("input.json", "w") as f:
    json.dump(data, f, indent=4)




# Load JSON file into Pandas dataframe
df = pd.read_json(json.dumps(data))

# Normalize the 'items' and 'discounts' columns
df_items = pd.json_normalize(data=df['orders'], record_path='items', meta=['order_number', 'staff_number','customer_number', ['discounts', 'VIP'], ['discounts', 'VIPDay95'], ['discounts', 'VIPDay123']])

# Rename columns
df_items = df_items.rename(columns={
    'item_number': 'Item Number',
    'item_name': 'Item Name',
    'quantity': 'Quantity',
    'cost': 'Cost',
    'order_number': 'Order Number',
    'staff_number': 'Staff Number',
    'number_of_items': 'Number of Items',
    'discounts.VIP': 'VIP Discount',
    'discounts.VIPDay95': 'VIPDay95 Discount',
    'discounts.VIPDay123': 'VIPDay123 Discount',
    'customer_number': 'Customer Number',
    'customer_name': 'Customer Name', 
    'customer_address': 'Customer Address', 
    'invoice_date': 'Invoice Date'
})

#df_items = df_items[df_items['Item Number']]
Hash_total_of_orders = df_items['Item Number'].sum()
# print(Hash_total_of_orders)
#print(total)

json_data = json.loads(open('input.json').read())
#print(json_data)
hash_total = 0
hash_list = []
staff_list = []

# Loop through the json data and append the hash list and staff list
for j in json_data['orders']:
    for k in j['items']:
        hash_total += k['item_number']
    hash_list.append(hash_total)
    staff_list.append(j['staff_number'])
    #print(hash_total)
    hash_total = 0   
    #print()
            
