from flask import Flask,render_template, flash, request, url_for, redirect, jsonify
from os import urandom #Secret key
app = Flask(__name__)

#Database MAnagement
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#Creating connectio to database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind =engine)
session = DBSession()

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
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html',restaurants = restaurants)

#Create new restaurant
@app.route('/restaurant/new', methods = ['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['newrest'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

#Edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET','POST'])
def editRestaurant(restaurant_id):
    EditedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        EditedRestaurant.name = request.form['editrest']
        session.add(EditedRestaurant)
        session.commit()
        flash("Restaurant Edited!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant = EditedRestaurant)

#Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        flash("Restaurant Deleted!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant = deletedRestaurant)


#Show Restaurant's menu
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant= restaurant, items = menu)

#Create new Menu's item
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    newname =""
    newcourse = ""
    newprice = ""
    newdescrip = ""
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['namemenu']: newname = request.form['namemenu']
        if request.form['coursemenu']: newcourse = request.form['coursemenu']
        if request.form['descripmenu']: newdescrip = request.form['descripmenu']
        if request.form['pricemenu']: newprice = request.form['pricemenu']
        newMenuItem = MenuItem(name = newname, course = newcourse, description = newdescrip,
                               price = newprice, restaurant_id =  restaurant_id)
        session.add(newMenuItem)
        session.commit()
        flash("New Menu Item Created!")
        return redirect(url_for('showMenu',restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant = restaurant)

#Edit Menu's item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id =  restaurant_id, id =  menu_id).one()
    if request.method == 'POST':
        if request.form['namemenu']:
            item.name = request.form['namemenu']
        if request.form['descripmenu']:
            item.description = request.form['descripmenu']
        if request.form['pricemenu']:
            item.price = request.form['pricemenu']
        if request.form['coursemenu']:
            item.course = request.form['coursemenu']
        session.add(item)
        session.commit()
        flash("Menu Item Edited!")
        return redirect(url_for('showMenu',restaurant_id =  restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant = restaurant, item = item)

#Delete Menu's item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete' , methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        flash("Menu Item Deleted!")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant = restaurant, item = item)

#API endpoints
#All restaurantas
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [restaurant.serialize for restaurant in restaurants])

#Restaurant's menu
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [item.serialize for item in menuItems])

# Specific Menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id, restaurant_id = restaurant_id).one()
    return jsonify(MenuItem = menuItem.serialize)


if __name__ == '__main__':
    app.secret_key = urandom(24)
    app.debug = True
    app.run(host = '0.0.0.0', port=8000)