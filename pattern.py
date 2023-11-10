num_lines = int(input("Enter the number of lines for the design: "))

text = "FORMULAQSOLUTIONS"
pattern = ""
for i in range(num_lines):
    spaces = " " * (2 * i)
    if i < num_lines - 3:
        text_part = text[i:num_lines - 1]
    elif i == num_lines - 3:
        text_part = text[i:num_lines - 1] + "RMUL"
    elif i == num_lines - 2:
        text_part = text[i:num_lines - 1] + "RMU"
    elif i == num_lines - 1:
        text_part = text[i:num_lines]

    pattern += spaces + text_part + "\n"
print(pattern)
