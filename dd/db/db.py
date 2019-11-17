import requests, json, sys # Allows the fetching and storing of the API calls
from math import radians, cos, sin, sqrt, atan2

# === Update the database from the Nova Scotia open data API ===
def updateDatabase(daycares):
    with open("dd/db/db.json", "w") as databaseFile:  # Opening database.json as truncate 
        json.dump(daycares, databaseFile) # Dump the data into the file using the json class

# === Get an updated version of the data from the API ===
def fetchDatabase():
    url = "https://data.novascotia.ca/resource/3j9v-yimg.json" # URL for API fetching
    daycares = requests.get(url).json() # Request is the raw request information
    updateDatabase(daycares) # Update the .json file 
    updateDatabase(fixCasing()) # Update the database again with the fixed data
    updateDatabase(indexify())
    

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

def getDaycare(index):
    database = getDatabase()
    for daycare in database:
        if daycare["index"] == index:
            return daycare

# === Index all of the daycares ===
def indexify():
    database = getDatabase() 
    index = 0 # Initialize an index count
    for daycare in database: # Run through every daycare in the database
        daycare["index"] = index # Add a new key 'index' which has a unique value for each daycare
        index += 1 # Increment the index for the next daycare
    return database # Return the indexed database

# Calculates the distance between two poistions, returns distance
def getDistance(lat1, lon1, lat2, lon2):
    R = 6373.0  # approximate radius of earth in km
    lat1 = radians(float(lat1)) # Must convert
    lat2 = radians(float(lat2))
    lon1 = radians(float(lon1)) # these all to
    lon2 = radians(float(lon2)) #floats then radians
    dlon = lon2 - lon1 # Get difference between longitudes
    dlat = lat2 - lat1 # Get difference between latitudes
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    # ^^^^^^^^^^^^^^ DO FANCY MATHS IDC ABOUT ^^^^^^^^^^^^^^^^^^^^^^
    return R * c

# Method to sort inputted array of dictionaries with "distance" key by distance
# THIS IS A PEICE OF SHIT, don't touch
def sortByDistance(nearby):
    notSorted = True
    noChange = True
    # print("LENGTH = " + str(len(nearby)), file=sys.stderr)
    i = 0
    while (notSorted):
        noChange = True
        # print("INDEX" + str(i), file=sys.stderr)
        if (i+1 == len(nearby) and noChange):
            # print("SORTED", file=sys.stderr)
            break
        if (i+1 >= len(nearby) and notSorted):
            i = 0
            # print("NOT SORTED", file=sys.stderr)
            continue
        if (int(nearby[i]["distance"]) <= int(nearby[i+1]["distance"])):
            i += 1
            # print("SKIP", file=sys.stderr)
            continue
        if (int(nearby[i]["distance"]) >= int(nearby[i+1]["distance"])):
            temp = nearby[i+1]
            nearby[i+1] = nearby[i]
            nearby[i] = temp
            i += 1
            noChange = False
            # print("SWAP", file=sys.stderr)
            continue
    return nearby

# Controller function to get the
def getByDistance(maxDistance, amount, user_geoData):
    userlat = user_geoData["latitude"]
    userlon = user_geoData["longitude"]
    database = getDatabase()
    nearby = []
    for daycare in database:
        if ('location' in daycare):
            distance = getDistance(userlat, userlon, daycare["location"]["latitude"], daycare["location"]["longitude"])
            # print(distance, file=sys.stderr)
            if (distance < maxDistance):
                daycare["distance"] = distance
                nearby.append(daycare)
    # print("SORTING NOW", file=sys.stderr)
    nearby = sortByDistance(nearby)
    return nearby[:amount]

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
# print(getDaycare(1))
