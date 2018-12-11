#1
def increase(num):
    num = num + 1
    return(num)
#2
def add(num1,num2):
    total = num1 + num2
    return(total)
#3
def add3(num1,num2,num3):
    total = num1 + num2 + num3
    return(total)
#4
def add5(num1,num2,num3,num4,num5):
    total = num1 + num2 + num3 + num4 + num5
    return(total)
#5 
def multiplewords(number,string):
    word_multiple = number * string
    return(word_multiple)
#6     
def multiplewords(number,string):
    word_multiple = number * (string + "," )
    word_multiple = word_multiple[:-1]
    return(word_multiple)
print(multiplewords(3,"dad"))
#7  just change "," inside the word_multiple variable  

