def risk5(lst):
    for i in lst:
        if i > 0:
            if i < 10:
                if i % 2 == 0:
                    print("Small even")
                else:
                    print("Small odd")
            else:
                if i % 3 == 0:
                    print("Large div by 3")
                elif i % 5 == 0:
                    print("Large div by 5")
                else:
                    print("Large other")
        else:
            print("Non-positive")
