from cs50 import get_float

while True:
    input = get_float("Change: ")
    if input > 0:
        break
input = input*100

q = int(input/25)
d = int((input-(q*25))/10)
n = int((input-((q*25)+(d*10)))/5)
c = int(input-((q*25)+(d*10)+(n*5)))
total = (q+d+n+c)
print(f"Total", total)
