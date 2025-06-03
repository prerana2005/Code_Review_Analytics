def risk3(n):
    result = 0
    for i in range(n):
        if i % 2 == 0:
            if i % 3 == 0:
                if i % 4 == 0:
                    if i % 5 == 0:
                        if i % 6 == 0:
                            if i % 7 == 0:
                                if i % 8 == 0:
                                    result += i
    return result
