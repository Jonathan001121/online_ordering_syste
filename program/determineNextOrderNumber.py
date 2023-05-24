# Group C
# Lau Kai Yeung 21214638​
# Le Ching Wa, Louis 22205276​
# Lee Wang, Ryan 20236700​
# Lau Shing Yuk 20203810​
# Tung Lok Yin, Jason 20203802​
# Chan Chi Hin, Jonathan 20202288

import random


def get_next_order_number(last_order_number):
    # Separate the prefix and number parts of the order number
    prefix, num = last_order_number.split('-')
    
    # Convert the number part to an integer
    num = int(num)
    
    # Check if the current order number is at the maximum value
    if prefix == 'Z' and num == 999999:
        # If so, return the first order number of the next prefix
        return 'AA-000001'
    elif prefix[-1] == 'Z' and num == 999999:
        # If the last character of the prefix is 'Z' and the number part is at the maximum value,
        # increment the prefix
        prefix = increment_prefix(prefix)
        # Reset the number part to 1
        num = 1
    elif num == 999999:
        # If the number part is at the maximum value, increment the prefix
        prefix = increment_prefix(prefix)
        # Reset the number part to 1
        num = 1
    else:
        # Otherwise, increment the number part
        num += 1
    
    # Combine the prefix and number parts and return the new order number
    return f"{prefix}-{num:06d}"
def returnRandomMoudule():
     return random.choice(['A', 'B', 'C'])

def increment_prefix(prefix):
    # If the prefix is a single letter, increment it
    if len(prefix) == 1:
        return chr(ord(prefix) + 1)
    
    # If the last character of the prefix is 'Z', recursively increment the prefix without the last character
    if prefix[-1] == 'Z':
        return increment_prefix(prefix[:-1]) + 'A'
    
    # Otherwise, increment the last character of the prefix
    return prefix[:-1] + chr(ord(prefix[-1]) + 1)
def main():
    last_order_number = 'A-567878'
    next_order_number = get_next_order_number(last_order_number)
    print(next_order_number)  # Output: A-567879

    last_order_number = 'Z-999999'
    next_order_number = get_next_order_number(last_order_number)
    print(next_order_number)  # Output: AA-000001

    last_order_number = 'BZ-999999'
    next_order_number = get_next_order_number(last_order_number)
    print(next_order_number)  # Output: AB-000001

if __name__ == "__main__":
    main()
