import requests, json

# Update the database from the Nova Scotia open data API
def updateDatabase():
    # Request is the raw request information
    request = requests.get("https://data.novascotia.ca/resource/3j9v-yimg.json")
    # Convert the request into json data
    daycares = request.json()
    # Opening database.json as truncate 
    with open("dd/db/db.json", "w") as databaseFile:
        # Dump the data into the file using the json class
        json.dump(daycares, databaseFile)
    # Close the file
    databaseFile.close()

# Return a dictionary containing the database
def getDatabase():
    # Open the file as read only
    with open("dd/db/db.json") as databaseFile:
        # Return the database file as a dictionary using the json class
        return json.load(databaseFile)

def getXElements(x):
    database = getDatabase()
    return database[:x]



# updateDatabase()
# daycares = getDatabase()
# daycares = getXElements(6)
# print(daycares)
