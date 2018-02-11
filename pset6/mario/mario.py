import cs50
while True:
    num = input("Input a height: ")
    if int(num) > 0 and int(num) < 23:
        break

for i in range(int(num)):
    print(" " * (int(num) - i - 1),end="")
    print("#" * (i + 1),end="")
    print("  ",end="")
    print("#" * (i + 1))
