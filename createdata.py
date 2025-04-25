from random import randrange
with open('planetdata.dat', 'w') as f:
    for n in range (int(input())):
        f.write(f'Body {n + 1},{randrange(1, 9)},{randrange(26, 29)},{randrange(500,75000)},{randrange(-2_000_000_000, 2_000_000_000)},{randrange(-2_000_000_000, 2_000_000_000)},{randrange(-100, 100)},{randrange(-100, 100)},{randrange(0, 255)} {randrange(0, 255)} {randrange(0, 255)}\n')
    f.close()