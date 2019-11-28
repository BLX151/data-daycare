import requests, json, sys
from math import radians, cos, sin, sqrt, atan2

# UPDATE DATABASE FILE
# ============================================================================================================
def updateDatabase(database):
    with open("dd/db/db.json", "w") as databaseFile:  # Opening database.json as truncate 
        json.dump(database, databaseFile) # Dump the data into the file using the json class
# ============================================================================================================

# FETCH UPDATED DATABASE FROM API
# ============================================================================================================
def fetchDatabase():
    return requests.get("https://data.novascotia.ca/resource/3j9v-yimg.json").json()
# ============================================================================================================

# RETURN DATABASE AS DICT
# ============================================================================================================
def getDatabase():
    with open("dd/db/db.json") as databaseFile: # Open the file as read only
        return json.load(databaseFile) # Return the database file as a dictionary using the json class
# ============================================================================================================

# GET DAYCARES MATCHING INDEXLIST
# ============================================================================================================
# TODO: Update so it returns daycares with matching indexes
def getDaycares(indexList):
    database = getDatabase() # Get the database
    matchingDaycares = []
    for daycare in database:
        if daycare['index'] in indexList:
            matchingDaycares.append(daycare)
    return matchingDaycares
    # The .json file is just a list of dictionaries.
    # This is split the list from the beginning to the x-th item in the list
# ============================================================================================================

# GET DAYCARE MATCHING INDEX
# ============================================================================================================
def getDaycare(index):
    database = getDatabase()
    for daycare in database:
        if daycare["index"] == index:
            return daycare
# ============================================================================================================

# INDEX DAYCARES
# ============================================================================================================
def indexDaycares():
    database = getDatabase() 
    index = 0 # Initialize an index count
    for daycare in database: # Run through every daycare in the database
        daycare["index"] = index # Add a new key 'index' which has a unique value for each daycare
        index += 1 # Increment the index for the next daycare
    return database # Return the indexed database
# ============================================================================================================

# CALCULATE DISTANCE BETWEEN TWO COORDINATES
# ============================================================================================================
def getDistance(lat1, lon1, lat2, lon2):
    R = 6373.0  # approximate radius of earth in km
    lat1 = radians(float(lat1)) # Must convert
    lat2 = radians(float(lat2)) # all of these
    lon1 = radians(float(lon1)) # into floats
    lon2 = radians(float(lon2)) # then to radians
    dlon = lon2 - lon1 # Get difference between longitudes
    dlat = lat2 - lat1 # Get difference between latitudes
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    # ^^^^^^^^^^^^^^ DO FANCY MATHS IDC ABOUT ^^^^^^^^^^^^^^^^^^^^^^
    return R * c # Return the distance between the two coords
# ============================================================================================================


# SORT DAYCARES BY DISTANCE
# ============================================================================================================
# TODO - update so it can sort by any criteria
# THIS IS A PEICE OF SHIT, don't touch, it works somehow
# could be refactored so it will sort by any term
def sortByDistance(nearby):
    notSorted, noChange, i = True, True, 0 # Set conditional variables
    while (notSorted): # As long as the list is not sorted
        noChange = True # Reset the noChange to default
        # If reach end of list and noChange has happened, then the list
        # must be sorted
        if (i+1 == len(nearby) and noChange):
            break # Exit the loop
        # If end of list and list is not sorted, reset sort again
        if (i+1 >= len(nearby) and notSorted):
            i = 0 # Reset the index to 0
            continue # Skip to next loop
        # If current daycare is closer than next daycare, skip
        if (int(nearby[i]["distance"]) <= int(nearby[i+1]["distance"])):
            i += 1
            continue
        # If current daycare is further than next daycare, swap
        if (int(nearby[i]["distance"]) >= int(nearby[i+1]["distance"])):
            temp = nearby[i+1]
            nearby[i+1] = nearby[i]
            nearby[i] = temp
            i += 1
            noChange = False # Indicate a change was made
            continue
    return nearby # Return the sorted array
# ============================================================================================================

# GET DAYCARES WITH CLOSEST DISTANCE
# ============================================================================================================
def getByDistance(maxDistance, amount, user_geoData):
    database = getDatabase()
    nearby = [] # Empty list
    for daycare in database:
        if ('location' in daycare): # Check to make sure it has a location
            distance = getDistance( # Get the distance between the two coords
                user_geoData["latitude"], user_geoData["longitude"], # User lat and lon
                daycare["location"]["latitude"], daycare["location"]["longitude"]) # Daycare lat and lon
            if (distance < maxDistance): # If the distance is less than maximum allowed distance
                daycare["distance"] = distance # Add a new key 'distance' to daycare
                nearby.append(daycare) # Append it to empty list
    nearby = sortByDistance(nearby) # Sort this list by distance
    return nearby[:amount] # Return on the first 'amount' of entires (i.e. 5)

# FIX FORMATTING ISSUES
# ============================================================================================================
# DO NOT TOUCH, THIS WORKS AS EXPECTED AND I DON'T REMEMBER HOW I DID IT
def fixFormatting():
    database = getDatabase()
    for daycare in database:
        if ('(' in daycare['facility_name'] ):
            name = daycare['facility_name']
            daycare['facility_name'] = name[:name.rfind('(') - 1]
        split = daycare['city'].split()
        city = ""
        for word in split:
            word = word.lower().capitalize()
            if city == "":
                city += word
            else:
                city +=  " " + word
        daycare['city'] = city
        split = daycare['address'].split()
        address = ""
        for word in split:
            word = word.lower().capitalize()
            if word.endswith("."):
                word = word[:-1]
            if address == "":
                address += word
            else:
                address += " " + word
        daycare['address'] = address
    return database
# This is a spaghetti mess...
# ============================================================================================================

# GET DAYCARES WHICH MATCH FILTERS
# ============================================================================================================
def filterDaycares(filters):
    database = getDatabase()
    matchingDaycares = []
    for daycare in database:
        if ('county' in filters and daycare["county"] != filters["county"]):
            continue
        if ('facility_type' in filters and daycare["facility_type"] != filters["facility_type"]):
            continue
        if ('max_capacity' in filters and 'total_licance_capacity' in daycare and int(daycare["total_licance_capacity"]) >= int(filters["max_capacity"]) ):
            continue
        if ('min_capacity' in filters and 'total_licance_capacity' in daycare and int(daycare["total_licance_capacity"]) >= int(filters['min_capacity']) ):
            continue
        if ('city' in filters and daycare["city"] != filters["city"]):
            continue
        if ('age_infant' in filters and daycare["age_infant"] != filters["age_infant"]):
            continue
        if ('age_toddler' in filters and daycare["age_toddler"] != filters["age_toddler"]):
            continue
        if ('age_preschool' in filters and daycare["age_preschool"] != filters["age_preschool"]):
            continue
        if ('age_school_age' in filters and daycare["age_school_age"] != filters["age_school_age"]):
            continue
        if ('prog_full_day' in filters and daycare["prog_full_day"] != filters["prog_full_day"]):
            continue
        if ('prog_part_day' in filters and daycare["prog_part_day"] != filters["prog_part_day"]):
            continue
        if ('annual_inspection' in filters and "annual_inspection" not in daycare):
            continue
        if ('annual_unannounced_inspection' in filters and "annual_unannounced_inspection" not in daycare):
            continue
        matchingDaycares.append(daycare['index'])

    return getDaycares(matchingDaycares)

# ============================================================================================================




# DEBUG
# ============================================================================================================
# fetchDatabase()
# daycares = getDatabase()
# daycares = getDaycares(6)
# print(daycares)
# print(getDaycare(1))
# ============================================================================================================
