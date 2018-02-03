food={"vegetables":["carrots","kale","cucumber","tomato"],"desserts":["cake","ice cream", "donut"]}
for hungry in food["vegetables"]:
	print("My favorite vegetable is " + hungry)

# Using the food variable write a loop to access and print the values for the desserts key in a sentence.
for sweet in food["desserts"]:
	print("We have desserts:", sweet)

cars={"sports":{"Volkswagon":"Porsche","Dodge":"Viper","Chevy":"Corvette"},"classic":{"Mercedes-Benz":"300SL","Toyota":"2000GT","Lincoln":"Continental"}}
for auto in cars["sports"]:
	print("My favorite sports car is a " + cars["sports"][auto])

# Using the cars variable write a loop to access and print the values for the classic key in a sentence.
for classic_cars in cars["classic"]:
	print("My favorite classic car is a", classic_cars)

dessert={"iceCream":["Rocky Road","strawberry","Pistachio Cashew","Pecan Praline"]}
# Write a loop to print all of the values for variable dessert in a sentence.
for food_dessert in dessert["iceCream"]:
	print(food_dessert)


soup={"soup":{"tomato":"healthy","onion":"bleh!","vegetable":"good for you"}}
# Write a loop to print all of the values for variable soup in a sentence.
for soup_opt in soup["soup"]:
  print(soup_opt, soup["soup"][soup_opt])