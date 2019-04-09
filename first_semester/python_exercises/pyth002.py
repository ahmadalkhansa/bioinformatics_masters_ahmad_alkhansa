#1
x = "fire and ice"
#2
print(x[2])
#3
print(x[4])
#5
print(x[1::2])
#6
print(x[::2])
#7
print(x[len(x)//2:])
#8
print(x[::-1])
#9
print(x.count("i")+x.count("e"))
#10
x = x.replace("and","&")
print(x)
#11,12,13
word = str(input("write whatever you want: "))
if x.find(word) == -1:
    check = "sorry, not available"
else:
    check = "yes we have"

print(check)
#14
print(x.find("e"))
#15
print(x.rfind("e"))
#17 
a_variable = "234 4329 7654 8923"
#18
a = "234 4329 7654 8923"
b = a.replace(" ", "")
c = [int(x) for x in b]
for y in c:
 print(y + 3)

                      
