from cs50 import get_string

letters = 0
words = 0
sentences = 0
text = get_string("Text: ")

for x in text:
    if x.isalpha() == True:
        letters = letters+1

for word in text.split():
    if word != None:
        words = words+1
for sentence in text:
    if (sentence == ".") or (sentence == "!") or (sentence == "?"):
        sentences = sentences+1

L = float((letters/words)*100)
S = float((sentences/words)*100)
grade = round(((0.0588 * L) - (0.296 * S) - 15.8))
if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
