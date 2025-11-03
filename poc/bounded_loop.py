def infinite_loop(*, fuel=100):
    i = 0
    while not fuel <= 0 and True:
        fuel = fuel - 1
        i += 1