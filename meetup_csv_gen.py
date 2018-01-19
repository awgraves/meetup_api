
import requests
import pandas as pd
import json
import datetime as dt
import time

#=========================================================================================
# Automatic CSV File Generator for Meetup.com API Data
# Created by: Andrew Graves
# Date: Jan 17, 2018
#=========================================================================================
"""Prompts user for API key, zipcode, and search radius (0 - 100 miles).  
Stores api key in api_key.txt for later user.
Exports a csv file containing rows with the following meetup group information:

- name of group
- group id
- city
- latitude of meetup location
- longitude of meetup location
- meetup category (Social, Tech, Arts, etc.)
- datetime of group creation
- status (active, grace)
- # of current members
- join mode (open, approval)
- # of previous events held
- datetime of most recently past event
- # of 'yes' rsvps for most recently past event
"""

# Meetup.com api instructions can be found here: https://www.meetup.com/meetup_api/docs/find/groups/

def get_api_key():
    """Checks if there is an api key specified in api_key.txt
    
    If none exists, prompts the user for one and stores the answer in the config file for next time.
    """
    with open("api_key.txt", "r+") as f: #open up the txt file and check whether the key is already there
        api_key = f.read()
        if len(api_key) < 5: #if user did not provide api key, prompt for key manually
            print("**(You can find your API key for meetup.com at https://secure.meetup.com/meetup_api/key/)")
            print(" ")
            key = input("API key: ")
        
            f.write(key) #write the user input to the api_key.txt file for later use
        
            return key

        else: #otherwise, use the API key from file and notify user
            print("***User API key is on file.***")
            print("")
            return api_key

def query_api():
    """Queries the meetup.com API and returns a list of dictionaries containing the requested info on meetup groups.  
    
    Responses are in batches of 200 entries. There is a time delay between reqs to not exceed the API rate limit.  
    
    Once we receive a response containing less than 200 entries, we know we have collected all information we need."""
    
    finished = False #we are just beginning!
    batch = 0 #set our first batch number
    raw_data = [] #create our list to eventually return
    
    while finished == False: #keep looping until we run out of data to find
        parameters = {"key":key, "sign":"true", "page":"200", "offset":batch, "zip":zip, "radius":radius, "only":"category,created,id,city,join_mode,last_event,members,name,past_event_count,status,lat,lon", "fields":"last_event,past_event_count"}

        response = requests.get("https://api.meetup.com/find/groups", params = parameters) #make the API request
        status = response.status_code #get the status of our request
        data = response.json() #convert the JSON data to python dictionaries
        
        print("Batch number: {}".format(batch+1))
        if status == 200: #things are ok
        	print("Server request: OK")
    
        if status == 401: #not ok
            print("Bad server request!")
        
        if status != 200 and status != 401: #else
        	print("Server request: Status Code {}".format(status))
        print("Number of groups returned: " + str(len(data)))
        print(" ")
        raw_data.append(data) #add the raw data to our list
        
        if len(data) < 200: #if we get less than 200 entries, stop the loop and return our final list
            finished = True
            print(" ")
            print("***Finished!***")
            return raw_data
        
        else: #if not, pause before making a new request with a new batch number
            time.sleep(0.25)
            batch+=1

def convert_to_df(raw_data):
    """Takes in a list of dictionaries, does some cleaning, and converts each to a pandas df.
    
    Returns a single dataframe combining all entries."""
    
    all_dfs = [] #master list of dataframes
    
    for i in range(0,len(raw_data)): #for each dictionary in our raw_data list
        utc_found = False #Search the dictionary for an entry containing the utc_offset value to adjust utc to local time
        while utc_found == False:
            for each in raw_data[i]:
                if "last_event" in each:
                    utc_offset = int(each["last_event"]["utc_offset"])
                    utc_found = True
                else:
                    next
        
        for each in raw_data[i]: #clean up each dictionary  
            if "category" in each: #correct the category name
                each["category"] = each["category"]["name"]
            
            each["created"] = each["created"] + utc_offset #correct the founding date to the local timezone
            
            if "past_event_count" in each: #if there is a past event counter make it an integer
                each["past_event_count"] = int(each["past_event_count"])
            
            if "last_event" in each: #if there was a past event, clean up the rsvp_count and the time of the event
                last = each["last_event"]
                each["last_rsvp"] = int(last["yes_rsvp_count"]) #make a new, separate dict key for the rsvp count
                each["last_event"] = int(last["time"] + utc_offset) #correct the last event date with UTC offset

            
        data = pd.DataFrame(raw_data[i]) #convert to a df
        all_dfs.append(data)#add to our master list
        
    return pd.concat(all_dfs) #return our final dataframe by combining all from the master list

def convert_to_dt(row):
    """Attempt to convert values to datetime objects.  Skip any values that give us trouble."""
    try:
        row = int(row)
        row = dt.datetime.utcfromtimestamp(row/1000)
    except:
        next
    return row


#initialize
banner = """
#=======================================================
# Automatic CSV File Generator for Meetup.com API Data
# Created by: Andrew Graves
# Date: Jan 17, 2018
#=======================================================

"""
print(banner)

#establish our api key
key = get_api_key()

#prompt user for a zip and search radius
zip = input("Zipcode to search: ")
radius = input("Search radius in miles (0.0 - 100.0): ")


#get our raw data
raw_data = query_api()        

#convert our raw data to a single pandas df
df = convert_to_df(raw_data)

#Reorder the columns
cols = ["name","id","city","lat","lon","category","created","status","members","join_mode","past_event_count","last_event","last_rsvp"]
df = df[cols]

#convert the timestamp values in "created" and "last_event" columns to datetime objects
df["created"] = df["created"].apply(convert_to_dt)
df["last_event"] = df["last_event"].apply(convert_to_dt)

#convert past_event_count and last_rsvp count to integers
df["past_event_count"] = df["past_event_count"].fillna(0).astype(int, errors="raise") #set any missing values to 0
df["last_rsvp"] = df["last_rsvp"].fillna(0).astype(int, errors="raise") #set any missing values to 0

#export our df and call it a day!
df.to_csv("meetup_groups.csv", index=False)
print("***Successfully exported file as 'meetup_groups.csv'***")
