# miscellaneous.py
# For the following exercises, pseudo-code is not required

# Exercise 1
# Create a list L of numbers from 21 to 39
# print the numbers of the list that are even
# print the numbers of the list that are multiples of 3

# Exercise 2
# Print the last two elements of L 

# Exercise 3
# What's wrong with the following piece of code? Fix it and 
# modify the code in order to have it work AND to have "<i> is in the list" 
# printed at least once

L = ['1', '2', '3']
for i in range(10)
    if i in L:
    print(i is in the list)
    else:
    print(i not found)    


# Exercise 4
# Read the first line from the sprot_prot.fasta file
# Split the line using 'OS=' as delimiter and print the second element
# of the resulting list 

# Exercise 5
# Split the second element of the list of Exercise 4 using blanks
# as separators, concatenate the first and the second elements and print
# the resulting string

# Exercise 6
# reverse the string 'asor rosa'

# Exercise 7
# Sort the following list: L = [1, 7, 3, 9]

# Exercise 8
# Create a new sorted list from L = [1, 7, 3, 9] without modifying L

# Exercise 9
# Write to a file the following 2 x 2 table:
# 2 4
# 3 6

#Answers:
#Exercise 1:

L = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
for n in range(0, len(L) + 1):
	even = L[n]
	g = L[n]%2
	if g == 0:
		print(g)

print(g)

for k in L:
	if int(k / 3) == float(k / 3):
		print(k)

print(k)

#Exercise 2:

print(L[-2::]

#Exercise 3:
L = ['1', '2', '3']
G = [str(i) for i in range(10)]
for i in G:
	for p in L:
		if int(i) == int(p):
			print(int(i),' is in the list')
		elif int(i) != int(p):
			print(int(i), ' not found')

#Exercise 4:
openfile = open('sprot_prot.fasta', 'r')
readfile = openfile.readlines()
for lines in readfile:
	if '>' == readfile[0]:
		print(readfile.split("OS = "))

#Exercise 6:
string = 'asor rosa'

print(string[-1::-1])

#Exercise 7:

L = [1, 7, 3, 9]
G= sorted(L)
print(G)

#Exercise 8:
L = [1, 7, 3, 9]
L = L.sort()
		

