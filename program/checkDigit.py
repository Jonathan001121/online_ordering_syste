def calculate_check_digit(staff_number, order_number, modulus):
    # Check if staff_number and order_number are strings of the correct lengths
    if len(staff_number) != 6 or len(order_number) != 6:
        raise ValueError("Invalid staff number or order number")

    # Validating staff number is numeric
    if not staff_number.isnumeric():
        raise ValueError("Invalid staff number")

    # Validating order number is numeric
    if not order_number.isnumeric():
        raise ValueError("Invalid order number")

    # Mapping modulus string to its integer value
    modulus_dict = {"A": 7, "B": 8, "C": 9}
    if modulus not in modulus_dict:
        raise ValueError("Invalid modulus")

    modulus = modulus_dict[modulus]

    # Padding the order number with zeros on the left if it is shorter than 6 digits
    order_number_str = str(order_number).zfill(6)

    # Calculating the check digit
    total = 0
    for i in range(len(staff_number)):
        total += int(staff_number[i]) * int(order_number_str[i])

    # Finding the check digit that makes total % modulus = 0
    check_digit = 0
    while (total + check_digit) % modulus != 0:
        check_digit += 1
        # If modulus is not found for check digit, return None
        if check_digit > 9:
            return None

    return check_digit

def extract_order_info(order_string):
    if len(order_string) < 15:
        raise ValueError("Invalid order number length")

    # Extracting the first 1 or 2 alphabets
    if order_string[0].isalpha() and order_string[1].isalpha():
        first_two_alphabets = order_string[:2]
    else:
        first_two_alphabets = order_string[:1]

    # Extracting the staff number
    staff_number = order_string[len(first_two_alphabets):len(first_two_alphabets)+6]

    # Extracting the modulus
    modulus = order_string[len(first_two_alphabets)+6]

    # Extracting the order number
    order_number = order_string[len(first_two_alphabets)+7:len(first_two_alphabets)+13]

    # Extracting the number of items
    number_of_items = int(order_string[-1])

    return first_two_alphabets, staff_number, modulus, order_number, number_of_items

order_string = "A123456B5678784"
first_two_alphabets, staff_number, modulus, order_number, number_of_items = extract_order_info(order_string)
# print("First two alphabets:", first_two_alphabets)
# print("Staff number:", staff_number)
# print("Modulus:", modulus)
# print("Order number:", order_number)
# print("Number of items:", number_of_items)

# check_digit = calculate_check_digit(staff_number, order_number, modulus)
# if check_digit is None:
#     print("No check digit found for the given modulus.")
# else:
#     print("Calculated check digit:", check_digit)
