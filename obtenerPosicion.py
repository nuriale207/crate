import time
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
import requests
from crate import client


def position():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    position = response.json()["iss_position"]
    return f'POINT ({position["longitude"]} {position["latitude"]})',position


def insert(connection):
    # New connection each time
    cursor = connection.cursor()
    try:
        point, posicion=position()
        direccion=get_address ( posicion["latitude"], posicion["longitude"] )
        cursor.execute(
            "INSERT INTO iss (position,address) VALUES (?,?)", [point, direccion],
        )
        print("INSERT OK")
    except Exception as err:
        print("INSERT ERROR: %s" % err)
        return

def get_address(lan, lon):
	try:
		geolocator = Nominatim(user_agent="altaruru_testgeopy")
		scoord = ("%s %s" % (lan, lon))
		location = geolocator.reverse(scoord)
		return location.address
	except:		
		debug.print_exception()
		return None	


def createDatabase(connection):
	
	cursor = connection.cursor()   
	try: 
		cursor.execute(
		        """CREATE TABLE iss(
		        timestamp TIMESTAMP GENERATED ALWAYS AS CURRENT_TIMESTAMP,
		        position GEO_POINT,
			address varchar(100))"""
		)
		print("DATABASE CREATED OK")
	except Exception as err:
		print("ERROR CREATING DATABASE: %s" % err)
		return

time.sleep(30)
try:
	connection = client.connect("crate:4200")
	print("CONNECT OK")

except Exception as err:
	print("CONNECT ERROR: %s" % err)

createDatabase(connection)

# Inserta 10 posiciones en la bd creada
for i in range(0,10):
    insert(connection)
    print("Sleeping for 5 seconds...")
    time.sleep(5)

