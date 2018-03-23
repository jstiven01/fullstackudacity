from flask import Flask,render_template, flash
from os import urandom #Secret key
app = Flask(__name__)

#Dictionaries for testing
#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
#####
## Show all restaurants
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	return render_template('restaurants.html',restaurants = restaurants)

#Create new restaurant
@app.route('/restaurant/new')
def newRestaurant():
    flash("New Restaurant Created!")
    return render_template('newrestaurant.html')

#Edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    flash("Restaurant Edited!")
    return render_template('editrestaurant.html', restaurant_name = restaurant["name"])

#Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    flash("Restaurant Deleted!")
    return render_template('deleterestaurant.html', restaurant_name=restaurant["name"])


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
    app.secret_key = urandom(24)
    app.debug = True
    app.run(host = '0.0.0.0', port=8000)