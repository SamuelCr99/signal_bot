import random

def get_random_quote():
    with open("quotes/quotes.tex") as f:
        lines = f.readlines()

    lines = [line for line in lines if line != '\n']
    lines = [line for line in lines if line != '\u200e\n']
    random_number = random.randint(5, len(lines)-2)
    return lines[random_number]