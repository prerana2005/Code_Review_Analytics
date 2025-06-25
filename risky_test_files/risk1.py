def risk1(x):
    if x > 0:
        if x < 100:
            for i in range(x):
                if i % 2 == 0:
                    print("Even")
                elif i % 3 == 0:
                    print("Divisible by 3")
                else:
                    if i % 5 == 0:
                        print("Divisible by 5")
                    elif i % 7 == 0:
                        print("Divisible by 7")
                    else:
                        print("Other")
        elif x == 100:
            print("Exactly 100")
        else:
            print("Too large")
    else:
        print("Non-positive number")
