import requests, json


# Update the database from the Nova Scotia open data API
def updateDatabase(daycares):
    # Opening database.json as truncate 
    with open("dd/db/db.json", "w") as databaseFile:
        # Dump the data into the file using the json class
        json.dump(daycares, databaseFile)
    # Close the file
    databaseFile.close()


def fetchDatabase():
# Request is the raw request information
    request = requests.get("https://data.novascotia.ca/resource/3j9v-yimg.json")
    # Convert the request into json data
    daycares = request.json()

    updateDatabase(daycares)
    fixedDatabase = fixCasing()
    updateDatabase(fixedDatabase)
    

# Return a dictionary containing the database
def getDatabase():
    # Open the file as read only
    with open("dd/db/db.json") as databaseFile:
        # Return the database file as a dictionary using the json class
        return json.load(databaseFile)


def getXElements(x):
    database = getDatabase()
    return database[:x]


def fixCasing():
    database = getDatabase()
    
    for daycare in database:
        split = daycare['city'].split()
        city = ""
        
        for word in split:
            word = word.lower().capitalize()
            
            if city == "":
                city = city + word
            else:
                city = city + " " + word
        
        daycare['city'] = city
    
    for daycare in database:
        split = daycare['address'].split()
        address = ""
        
        for word in split:
            word = word.lower().capitalize()

            if word.endswith("."):
                word = word[:-1]
            
            if address == "":
                address = address + word
            else:
                address = address + " " + word
        
        daycare['address'] = address

    return database

# fetchDatabase()
# daycares = getDatabase()
# daycares = getXElements(6)
# print(daycares)
