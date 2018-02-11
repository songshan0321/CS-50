import math

while True:
    inp = float(input("How much change is owed? "))
    if inp >= 0:
        break

owed = inp* 100
counter = 0

while True:
    if owed > 25:
        counter += math.floor(owed/25)
        owed = owed % 25
    elif owed > 10:
        counter += math.floor(owed/10)
        owed = owed % 10
    elif owed > 5:
        counter += math.floor(owed/5)
        owed = owed % 5
    elif owed == 0:
        break
    else:
        counter += owed
        owed = 0
print(int(counter))


