"""
a. Write two new functions named my_funct and my_funct2. The first function has no arguments and the second function should accept one argument. Each function should have at least one print statement.

b. Call the new functions passing in data for my_funct2.
"""
print ("I'm not a function")

def my_function():
	print("Hey I'm a function!")
        

def brett(val):
	for i in range(val):
		print("I'm a function with args!")
    
def new_func(data):
	data2= "my data is " + str(data)
	return (data2)

def calc(num,num2):
	var=num * num2
	print(var)

def my_funct():
	print("Hello everyone!")
	my_funct2(name)
	
def my_funct2(name_input):
	print("My name is " + name + "!")

my_function()
brett(5)
my_data=new_func("happy")
print(my_data)
calc(5,10)
name = "Marco"
my_funct()
