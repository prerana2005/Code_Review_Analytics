def risk4(x):
    if x > 10:
        if x < 20:
            if x % 2 == 0:
                print("Even and between 10 and 20")
            else:
                print("Odd and between 10 and 20")
        elif x < 30:
            if x % 3 == 0:
                print("Divisible by 3 and between 20 and 30")
            else:
                print("Between 20 and 30 but not divisible by 3")
    else:
        if x > 0:
            if x == 5:
                print("Exactly 5")
            else:
                print("Between 0 and 10 but not 5")
        else:
            print("Zero or negative")
