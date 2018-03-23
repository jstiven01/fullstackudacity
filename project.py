#First Flask Application
from flask import Flask , render_template, request, redirect, url_for, flash, jsonify
#Database MAnagement
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind =engine)
session = DBSession()

#Making a API Endpoint (Get Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
	return jsonify(MenuItem = item.serialize)
	 

#Initialize web server
#Coding different functions website
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
        
    return render_template('menu.html',restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
		newItem = MenuItem(name = request.form['nameitem'],restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New menu item created!")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one()
    if request.method == 'POST':
		if request.form['nameitem']:	       
		   editedItem.name = request.form['nameitem']		
		session.add(editedItem)
		session.commit()
		flash("Menu item edited!")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html',restaurant_id = restaurant_id, menu_id = menu_id, menu_name = editedItem.name)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one()
    if request.method == 'POST':	
		session.delete(deletedItem)
		session.commit()
		flash("Menu item deleted!")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html',restaurant_id = restaurant_id, menu_id = menu_id, item_name = deletedItem.name)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'	
	app.debug = True
	app.run(host = '0.0.0.0', port=5000)
	
