from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurants"):

            #Initialize Session in Restaurant DB
            engine = create_engine('sqlite:///restaurantmenu.db')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind =engine)
            session = DBSession()

            #consulting all restaurants
            allrest = session.query(Restaurant).all()    
            
            #Sending response to client
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            message = ""
            message += "<!DOCTYPE html>"
            message += "<html>"
            message += "<head><style>"
            message += '''input[type=submit] {
                         background:none!important;
                         color:blue;
                         border:none; 
                         padding:0!important;
                         font: inherit;
                         font-size:18pt;
                         /*border is optional*/
                         border-bottom:1px solid blue; 
                         cursor: pointer;
                    }'''
            message += "</head></style>"
            message += "<body>"
            for restaurant in allrest:
                message += "<h1>"+restaurant.name+"</h1>"
                message += "<form method='POST' enctype='multipart/form-data' action='/edit'>"
                message += '''<input value="%s" type="hidden" name="editrest1">\
                           <input type="submit" value="Edit"></form>''' % restaurant.id
                message += "<form method='POST' enctype='multipart/form-data' action='/delete'>"
                message += '''<input value="%s" type="hidden" name="delrest1">\
                           <input type="submit" value="Delete"></form>''' % restaurant.id
            message += "<h2><a href='/new'>Make a New Restaurant Here</a></h2>"
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return

        if self.path.endswith("/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            message = ""
            message += "<!DOCTYPE html>"
            message += "<html><body>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/new'><h1>Make a New Restaurant</h1>\
                          <input name="newrest" type="text" ><input type="submit" value="Create"></form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            #Fields contains information about HTML form
            fields={}

            # Initialize Session in Restaurant DB
            engine = create_engine('sqlite:///restaurantmenu.db')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            session = DBSession()


            # Response
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)

            if self.path.endswith("/new"):
                #Getting info of button submit
                messagecontent = fields.get('newrest')

                #Adding new restaurant to database
                NewRestaurant = Restaurant(name = messagecontent[0])
                session.add(NewRestaurant)
                session.commit()

                #Returning message HTML
                output = ""
                output += "<!DOCTYPE html>"
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/new'><h1>Make a New Restaurant</h1>\
                                          <input name="newrest" type="text" ><input type="submit" value="Create"></form>'''
                output += "<h4>Restaurant %s was added succesfully</h4>" % messagecontent[0]
                output += "<h2><a href='/restaurants'>Go to Restaurants</a></h2>"
                output += "</body></html>"

                self.wfile.write(output)

            if self.path.endswith("/edit"):
                #Getting info of button submit
                print "hola post ", self.path ,fields.get('editrest1')
                messagecontent = fields.get('editrest1')

                if messagecontent is not None:
                    msgid = messagecontent[0]
                    changerest = session.query(Restaurant).filter_by(id = msgid).one()
                    msg = changerest.name
                else:
                    messagecontent = fields.get('editrestid')
                    msgid = messagecontent[0]
                    Updatedrest = session.query(Restaurant).filter_by(id = msgid).one()
                    messagecontent = fields.get('editrest2')
                    msg=messagecontent[0]
                    Updatedrest.name = msg
                    session.add(Updatedrest)
                    session.commit()
                    msg += " was updated"


                #Returning message HTML
                output = ""
                output += "<!DOCTYPE html>"
                output += "<html><body>"
                output += "<h1>Edit Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/edit'><h2>%s</h2>''' % msg
                output += '''<input value="%s" type="hidden" name="editrestid">''' %msgid
                output += '''<input name="editrest2" type="text" ><input type="submit" value="Edit"></form>'''
                output += "<h2><a href='/restaurants'>Go to Restaurants</a></h2>"
                output += "</body></html>"

                self.wfile.write(output)

            if self.path.endswith("/delete"):
                #Getting info of button submit
                print "hola post ", self.path ,fields.get('delrest1')
                messagecontent = fields.get('delrest1')

                if messagecontent is not None:
                    msgid = messagecontent[0]
                    delrest = session.query(Restaurant).filter_by(id = msgid).one()
                    msg = delrest.name + '?'
                else:
                    messagecontent = fields.get('delrestid')
                    msgid = messagecontent[0]
                    Deletedrest = session.query(Restaurant).filter_by(id = msgid).one()
                    session.delete(Deletedrest)
                    session.commit()
                    msg = Deletedrest.name + " was deleted"



                #Returning message HTML
                output = ""
                output += "<!DOCTYPE html>"
                output += "<html><body>"
                if fields.get('delrest1') is not None:
                    output += "<h1>Are you sure you want to delete </h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/delete'><h2>%s</h2>''' % msg
                output += '''<input value="%s" type="hidden" name="delrestid">''' %msgid
                output += '''<input type="submit" value="Delete"></form>'''
                output += "<h2><a href='/restaurants'>Go to Restaurants</a></h2>"
                output += "</body></html>"

                self.wfile.write(output)

            print output

        except:
            pass


def main():
    try:
        port = 5000
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
