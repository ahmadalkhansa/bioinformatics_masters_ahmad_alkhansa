
#1 how to add a column on specific position
'''
T = open("table1.txt")
out_T = open('table-1.out', 'w')

table = []

for line in T:
    table.append(line.split())

exp5 = ['5', '17', '17', '2', '13']
table.insert(2, exp5)

for row in table:
    out_T.write('\t'.join(row) + '\n')

out_T.close()

print(table)
'''

#2 how to replace a column
'''
T = open("table1.txt")
table = []

for line in T:
    table.append(line.split())

columns = list(zip(*table))

columns.pop(3)
columns.insert(3, ['gene3', '20', '20', '20'])

rows = zip(*columns)

for elem in rows:
    print('\t'.join(elem))
'''

#3 sort the lists according to elements' positions selected
'''
from operator import itemgetter

data = [
[5, 10, 4, 3, 2],
[6, 7, 11, 9, 10],
[44, 66, 1, 81]
]

data_sorted = sorted(data, key = itemgetter(2))

print(data_sorted)
'''
