#1
a = [4,8,-9,"the"]
b = ["silent force",4.67,9]
c = a + b
print(c)
#2
x = "234 4329 7654 8923"
y = x.replace(" ","")
z = [int(p) + 3 for p in y]
print(z)
#3
r = "23|64|354|-123"
e = r.replace("|","")
d = e.replace("-","")
w = int(d)
print(w)
#4
k = "-1-987-6823-8261"
#5
g = [3.14, 6.333, 98.12, 23]
print(','.join(str(x) for x in g))
#6

