# Group C
# Lau Kai Yeung 21214638​
# Le Ching Wa, Louis 22205276​
# Lee Wang, Ryan 20236700​
# Lau Shing Yuk 20203810​
# Tung Lok Yin, Jason 20203802​
# Chan Chi Hin, Jonathan 20202288


# Mall dollars calculation method
def calculate_mall_dollars(total:float) -> float:
    mall_dollars = 0.0
    # check if total is greater than or equal to 500
    if total >= 500 and total <= 999:
        # calculate mall dollars *0.002 if total is greater than or equal to 500
        mall_dollars=total*0.002
    elif total >= 1000:
        # calculate mall dollars *0.0025 if total is greater than or equal to 1000
        mall_dollars=total*0.0025
    
    return mall_dollars
