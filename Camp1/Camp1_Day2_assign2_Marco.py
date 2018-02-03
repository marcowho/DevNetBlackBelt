"""
Libraries and Functions always come in handy to developers by allowing reusability of existing code. 
There are certain well known inherent libraries that you have access to after installing python. 
By using these libraries and functions in them, write a program to guess a randomly generated number between 1 and 10. 

For Example: 

Guess the number: 4
Wrong, try again! 

Guess the number: 8
Correct! 

Hint: Figure out which library the “randint” function belongs to.  
"""

import random

def user_number_guess(random_num):
	prompt = "Guess the number (1 - 10): "
	number = 0
	while number != random_num:
		number = int(input(prompt))
		if number != random_num:
			print("Wrong, try again!")
		else:
			print("Correct!")

def main():
	user_number_guess(random.randrange(1, 10))

main()