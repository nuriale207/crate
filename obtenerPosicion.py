import time

import requests
from crate import client


def position():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    position = response.json()["iss_position"]
    return f'POINT ({position["longitude"]} {position["latitude"]})'


def insert(connection):
    # New connection each time
    cursor = connection.cursor()
    try:
        
        cursor.execute(
            "INSERT INTO iss (position) VALUES (?)", [position()],
        )
        print("INSERT OK")
    except Exception as err:
        print("INSERT ERROR: %s" % err)
        return


def createDatabase(connection):
	
	cursor = connection.cursor()   
	try: 
		cursor.execute(
		        """CREATE TABLE iss(
		        timestamp TIMESTAMP GENERATED ALWAYS AS CURRENT_TIMESTAMP,
		        position GEO_POINT)"""
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

try:
        cursor = connection.cursor()   
        cursor.execute(
            "DROP TABLE iss"
        )
        print("DROP OK")
except Exception as err:
        print("DROP ERROR: %s" % err)

createDatabase(connection)

# Inserta 10 posiciones en la bd creada
for i in range(0,10):
    insert(connection)
    print("Sleeping for 5 seconds...")
    time.sleep(5)

