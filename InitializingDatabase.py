from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind =engine)

session = DBSession()

#Inserting data
MyFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(MyFirstRestaurant)
session.commit()

#Consulting data
session.query(Restaurant).all()

#Inserting data (other table)
cheesepizza = MenuItem(name = "Cheese Pizza", 
                        description = "Made with all natural ingredients and \
                        fresh mozzarella", course = "Entree", price = "$8.99",\
                        restaurant = MyFirstRestaurant)
session.add(cheesepizza)
session.commit()

#Consulting data
session.query(MenuItem).all()

#Reading data
firstResult = session.query(Restaurant).first()
#firstResult.name output element's name

#Adding many restaurants and menu items
#python lotsofmenus.py


#Update Process
#1.Find item (filter_by returns a collection)
veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
#iterating over the collection
for veggieBurger in veggieBurgers:
    print veggieBurger.id    
    print veggieBurger.name
    print veggieBurger.description
    print veggieBurger.course
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n" 

#filter the item to update.
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2).one()
print UrbanVeggieBurger.price
UrbanVeggieBurger.price = "$2.99"
session.add(UrbanVeggieBurger) ##2.Reset the value add is useful for creating and updating
session.commit()

#Delete Process
spinach = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
print spinach.id
print spinach.name
session.delete(spinach)
session.commit()

