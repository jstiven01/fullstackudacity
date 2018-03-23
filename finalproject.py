from flask import Flask
app = Flask(__name__)

## Show all restaurants
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	return "This page will show all restaurants"

#Create new restaurant
@app.route('/restaurant/new')
def newRestaurant():
	return "This page will allow to create a new restaurant"

#Edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	return "This page will edit the restaurant %s" % restaurant_id

#Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	return "This page will delete the restaurant %s" % restaurant_id

#Show Restaurant's menu
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	return "This page will show the menu of restaurant %s" % restaurant_id

#Create new Menu's item
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	return "This page will allow to create a new Menu's item of restaurant %s" % restaurant_id

#Edit Menu's item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	return "This page will edit Menu's item %s of restaurant %s" % (menu_id, restaurant_id)

#Delete Menu's item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	return "This page will delete Menu's item %s of restaurant %s" % (menu_id, restaurant_id,)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port=8000)