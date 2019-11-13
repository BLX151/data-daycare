import requests, json # Allows the fetching and storing of the API calls

# === Update the database from the Nova Scotia open data API ===
def updateDatabase(daycares):
    with open("dd/db/db.json", "w") as databaseFile:  # Opening database.json as truncate 
        json.dump(daycares, databaseFile) # Dump the data into the file using the json class

# === Get an updated version of the data from the API ===
def fetchDatabase():
    url = "https://data.novascotia.ca/resource/3j9v-yimg.json" # URL for API fetching
    request = requests.get(url) # Request is the raw request information
    daycares = request.json() # Convert the request into json data
    updateDatabase(daycares) # Update the .json file 
    fixedDatabase = fixCasing() # Fix the upper and lowercase shitshow that is the original file
    updateDatabase(fixedDatabase) # Update the database again with the fixed data
    

# === Return a dictionary containing the database ===
def getDatabase():
    with open("dd/db/db.json") as databaseFile: # Open the file as read only
        return json.load(databaseFile) # Return the database file as a dictionary using the json class

# === Return x elements from beginning of the list ====
# TODO: Update it so it will fetch x elements based on a search query
def getXElements(x):
    database = getDatabase() # Get the database
    return database[:x]
    # The .json file is just a list of dictionaries.
    # This is split the list from the beginning to the x-th item in the list

# === Fixes the casing from the original dataset. It doesn't display how we want it to. ===
# DO NOT TOUCH, THIS WORKS AS EXPECTED AND I DON'T REMEMBER HOW I DID IT
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
# This is a spaghetti mess...

# === DEBUG STATEMENTS ===
# fetchDatabase()
# daycares = getDatabase()
# daycares = getXElements(6)
# print(daycares)
