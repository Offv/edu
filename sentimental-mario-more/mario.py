from cs50 import get_int

while True:
    try:
        height = int(input("Height: "))
        if (height >= 1) and (height <= 8):
            break
    except:
        print("", end="")

spaces = 1
# prints newline
for j in range(height):

    # prints spaces
    for spaces in range(height-j-1):
        print(" ", end="")

    # prints hashes
    for i in range(j+1):
        print("#", end="")
    print("  ", end="")
    for k in range(j+1):
        print("#", end="")

    print()
