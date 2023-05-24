import json,os
import pandas as pd
import datetime
import hashTotal as ht
from mallsDollar import calculate_mall_dollars
import determineNextOrderNumber as dNON
import extract_data as ed
import checkDigit as cd
from nameAdress import name_address

# Function to calculate the delivery fee
def calculate_delivery_fee(sub_total):
    if sub_total >= 500:
        return 0
    else:
        return round(0.05 * sub_total, 2)

# Function to calculate the total cost
def calculate_total_cost(sub_total, discount1, discount2, delivery_fee):
    return round(sub_total - (sub_total* discount1) - (sub_total* discount2) + delivery_fee, 2)

# Main function for cost verification
def cost_verification(order_number, df, outputFile, index):
    order_df = df[df['Order Number'] == order_number]  # filter DataFrame to only include rows with matching order number
    items_total = (order_df['Cost'] * order_df['Quantity']).tolist() # Get the total cost of each item
    sub_total = sum(items_total)

    discount1 = order_df['VIPDay95 Discount'].min()
    discount2 = order_df['VIPDay123 Discount'].min()
    customer_number = order_df['Customer Number'].min()

    # Prevent a list more than 9 (should be checked before using this method)
    if len(items_total) > 9:
        print("Error: Maximum number of items exceeded (Maximum <= 9).")
        return
        
    # Calculate the total cost
    delivery_fee = calculate_delivery_fee(sub_total)
    total_cost = calculate_total_cost(sub_total, discount1, discount2, delivery_fee)
    mall_dollars = calculate_mall_dollars(total_cost)
    (name,address,invoice) = name_address(customer_number) # Storing the customer data by nameAdress.
    if total_cost >= 500 and total_cost <= 999:
        mall_dollars_percentage= "0.002"
    elif total_cost >= 1000:
        mall_dollars_percentage= "0.0025"
    else:
        mall_dollars_percentage= "0.00"

    modulus=dNON.returnRandomMoudule()

    order_no = ""
    if (order_number[0].isalpha() and order_number[1].isalpha()): order_no += order_number[0:2]
    else: order_no += order_number[0:1]
    order_no += ed.staff_list[0][0:] + str(modulus)

    # Write details in the given audit file
    outputFile.write("Order " + str(index) + " details\n")
    outputFile.write("Order_Number           " + order_no[:-1] + "\n")
    outputFile.write("Agency_number          " + ed.staff_list[0][0:] + "\n")
    outputFile.write("Modulus_number         " + modulus + "\n")
    outputFile.write("Total                  " + str(total_cost) + "\n")
    outputFile.write("Hash Total             " + str(ed.hash_list[0]) + "\n")
    outputFile.write("\n")

    # Print the receipt with "======" lines and using keywords
    print("====================================")
    print(f"Invoice Date: ({invoice})    Receipt: ({order_number})")
    print(f"Customer Number: {customer_number}")
    print("Sub-Total: $ {:.2f}".format(sub_total))
    discount1=sub_total*discount1
    discount2=sub_total*discount2
    print("Discount 1: $ {:.2f}".format(discount1))
    print("Discount 2: $ {:.2f}".format(discount2))
    print("Delivery Fee: $ {:.2f}".format(delivery_fee))
    print("Total: $ {:.2f}".format(total_cost))
    print("Mall Dollars: $ {:.2f}".format(mall_dollars))
    print("Hash Total:",ed.hash_list[0])

    # Arrange the order no.
    order_no = ""
    if (order_number[0].isalpha() and order_number[1].isalpha()): order_no += order_number[0:2]
    else: order_no += order_number[0:1]
    order_no += ed.staff_list[0][1:] + str(modulus)
    order = ""
    if (order_number[0].isalpha() and order_number[1].isalpha()): 
        order_no += order_number[3:9]
        order = order_number[3:9]
    else: 
        order_no += order_number[2:8]
        order = order_number[2:8]
    staff_no = ed.staff_list[0][0:]
    check_digit = cd.calculate_check_digit(staff_no, order, modulus)

    items_name = list(order_df['Item Name'].tolist())
    items_quantity = list(order_df['Quantity'].tolist())
    items_cost = list(order_df['Cost'].tolist())

    order_no += str(len(items_name))
    order_no += "("+ str(check_digit) +")"
    print(f"Order No. {order_no}")
    # print(str(modulus))
    path = "./invoice"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The inovice directory is created!")

    # Write the invoice with the arranged order no.    
    print("The new directory is created!")
    invoiceFile = open(f"./invoice/Invoice{order_no}.txt", "w")
    invoiceFile.write(f"Invoice Date: {invoice}    Order No.: {order_no}\n\n")
    invoiceFile.write(f"Customer Number: {customer_number}\n\n")
    items = list(order_df['Item Number'].tolist())
    
    for i in range(len(items)):
        invoiceFile.write(f"{items[i]}.     {items_name[i]}    {items_quantity[i]}    $ {items_cost[i]*items_quantity[i]}\n")
    invoiceFile.write(f"\nShipping To\n")
    invoiceFile.write(f"    Customer Name: {name}\n")
    invoiceFile.write(f"    Customer Address: {address}\n\n")
    invoiceFile.write("SubTotal: $ {:.2f}\n".format(sub_total))
    invoiceFile.write("    VIP: -$ {:.2f}\n".format(discount1))
    invoiceFile.write("    VIPAY95: -$ {:.2f}\n".format(discount2))
    if (delivery_fee > 0): invoiceFile.write("    Delivery Fee: $ {:.2f}\n".format(delivery_fee))
    else: invoiceFile.write("    Delivery Fee: FREE\n")
    invoiceFile.write("    Total: $ {:.2f}\n".format(total_cost))

    # Pop from list in extract data
    ed.hash_list.pop(0)
    ed.staff_list.pop(0)

    # Print the calculation details
    print("\nCalculation Details:")
    print("- Sub-Total: Sum of items total = $ {:.2f}".format(sub_total))
    print("- Discount 1: Discount 1 = $ {:.2f}".format(discount1) + " applied to the Sub-Total")
    print("- Discount 2: Discount 2 = $ {:.2f}".format(discount2) + " applied to the Sub-Total")
    print("- Delivery Fee: Delivery Fee depends on the Sub-Total and is calculated as follows:")
    print("  - If Sub-Total >= 500, then Delivery Fee = $0")
    print("  - If Sub-Total < 500, then Delivery Fee = 5% of Sub-Total, rounded to 2 decimal places")
    print("- Total: Sub-Total - Discount 1 - Discount 2 + Delivery Fee")
    print(f"- Total: ${sub_total:.2f} - ${sub_total*discount1:.2f} - ${sub_total*discount2:.2f} + ${delivery_fee:.2f} = ${total_cost:.2f}")
    print(f"- Mall Dollars: Total * {mall_dollars_percentage} = ${total_cost:.2f} * {mall_dollars_percentage} = ${mall_dollars:.2f}")
    now = datetime.datetime.now()
    # Get the current date
    date = now.date()
    print("Current date:", date)

    # Get the current time
    time = now.time()
    print("Current time:", time)  
    print("====================================")
    ht.Number_of_orders += 1  # The purporse for counting the number of items from hashTotal.py

def main():
    df_items=ed.df_items
    # Get all unique order numbers
    order_numbers = df_items['Order Number'].unique()

    outputFileName = "audited_file.txt"
    outputFile = open(outputFileName, "w")
    outputFile.write("Number_of_orders       " + str(len(order_numbers)) + "\n")
    outputFile.write("Hash_total_of_orders   " + str(ed.Hash_total_of_orders) + "\n\n")
    index = 1
    
    # Call cost_verification function for each order number
    for order_number in order_numbers:
        cost_verification(order_number, df_items, outputFile, index)
        index+=1
        
    outputFile.close()
if __name__ == "__main__":
    main()
