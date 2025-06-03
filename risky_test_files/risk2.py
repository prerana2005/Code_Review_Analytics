def risk2(data):
    for item in data:
        if isinstance(item, int):
            if item % 2 == 0:
                if item % 3 == 0:
                    print("Div by 2 and 3")
                elif item % 5 == 0:
                    print("Div by 2 and 5")
                else:
                    print("Only even")
            elif item % 7 == 0:
                print("Div by 7")
            else:
                print("Odd number")
