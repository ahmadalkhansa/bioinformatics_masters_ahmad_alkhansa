original = "234 4329 7654 8923"
no_space = original.replace(" ", "")
list = []

for digit in no_space:
    list.append(int(digit))

new_list = [x+3 for x in list]

new_no_space = "".join(str(e) for e in new_list)

print(new_no_space)

