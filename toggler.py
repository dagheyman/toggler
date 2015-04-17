#!/usr/bin/env python

import requests
import ConfigParser 
import sys
import json
import datetime

# Load configs
config = ConfigParser.ConfigParser()
config.read("./conf.ini")
api_token = config.get("ConfigSection", "api_token")
workspace_id = config.get("ConfigSection", "workspace_id")
sick_project_id = config.get("ConfigSection", "sick_project_id")

def fillUpFromToday():
    dateOfLatestEntry = findLatestEntry()
    print dateOfLatestEntry

def findLatestEntry():
    keepGoing = True
    count = 0
    while keepGoing:
        today = datetime.date.today() - datetime.timedelta(days=count)
        todayInIso = today.isoformat()
        print "Will now try " + todayInIso
        url = "https://www.toggl.com/api/v8/time_entries?start_date=" + todayInIso + "T00:00:00.000Z" + "&end_date=" + todayInIso + "T23:00:00.000Z"
        r = requests.get(url, auth=(api_token, "api_token"))
        if r.json():
            print "Found an entry for " + todayInIso + ". Will stop trying now."
            return today
            keepGoing = False
        count += 1


# Prints all the projects and id's for the current workspace
def printAllProjects():
    url = "https://www.toggl.com/api/v8/workspaces/" + workspace_id + "/projects" 
    r = requests.get(url, auth=(api_token,"api_token"))
    for project in r.json():
        print "#  " + str(project["id"]) + "  #  " + project["name"]

# Registers 8 hours of sickness for today on the predefined sick-project
def registerSickToday():
    url = "https://www.toggl.com/api/v8/time_entries"
    today = datetime.date.today().isoformat()
    data = {"time_entry":{"duration":28800,"start":today+"T07:00:00.000Z","pid":sick_project_id,"created_with":"toggler.py"}}
    r = requests.post(url, data=json.dumps(data), auth=(api_token, "api_token"))
    print "Registered sick today."

# Program entry
commands = { "projects" : printAllProjects, "sick" : registerSickToday, "fillup" : fillUpFromToday }
try:
    command = sys.argv[1]
    commands[command]()
except (KeyError, IndexError):
    print "No such command."

