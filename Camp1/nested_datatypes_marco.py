food={"vegetables":["carrots","kale","cucumber","tomato"],"desserts":["cake","ice cream", "donut"]}
print("My favorite vegetable is " + food["vegetables"][0])
print("My favorite dessert is " + food["desserts"][1])
# print donut
print("My favorite dessert is " + food["desserts"][2])

cars={"sports":{"Volkswagon":"Porsche","Dodge":"Viper","Chevy":"Corvette"},"classic":{"Mercedes-Benz":"300SL","Toyota":"2000GT","Lincoln":"Continental"}}
print("My favorite sports car is a Dodge " + cars["sports"]["Dodge"])
print("My favorite classic car is a Lincoln " + cars["classic"]["Lincoln"])
# print classic
print("My favorite cars are " + cars["classic"]["Mercedes-Benz"] + ", " + cars["classic"]["Toyota"] + " and " + cars["classic"]["Lincoln"] )


dessert={"iceCream":["Rocky Road","strawberry","Pistachio Cashew","Pecan Praline"]}
print("The values for dessert are " + dessert["iceCream"][0] + ", " + dessert["iceCream"][1] + ", "+ dessert["iceCream"][2] + ", " + dessert["iceCream"][3])

soup={"soup":{"tomato":"healthy","onion":"bleh!","vegetable":"good for you"}}
print("The soup are made with " + soup["soup"]["tomato"] + " tomato, " + soup["soup"]["onion"] + " onion, which are the vegetables "+ soup["soup"]["vegetable"])
