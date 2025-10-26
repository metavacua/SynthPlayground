def high_complexity_function(*, fuel=100):
    i = 0
    while not fuel <= 0 and i < 10:
        fuel = fuel - 1
        j = 0
        while not fuel <= 0 and j < 5:
            fuel = fuel - 1
            print(f'i: {i}, j: {j}')
            j += 1

high_complexity_function()
