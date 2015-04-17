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

# Prints all the projects and id's for the current workspace.
def printAllProjects():
    url = "https://www.toggl.com/api/v8/workspaces/" + workspace_id + "/projects" 
    r = requests.get(url, auth=(api_token,"api_token"))
    for project in r.json():
        print str(project["id"]) + "  -  " + project["name"]

# Registers 8 hours of sickness for today on the predefined sick-project.
def registerSickToday():
    url = "https://www.toggl.com/api/v8/time_entries"
    today = datetime.date.today().isoformat()
    data = {"time_entry":{"duration":28800,"start":today+"T07:00:00.000Z","pid":sick_project_id,"created_with":"toggler.py"}}
    r = requests.post(url, data=json.dumps(data), auth=(api_token, "api_token"))
    print "Registered sick today."

# Register work for all empty days until today, using the first argument as project id.
def fillUpFromToday():
    project_id = sys.argv[2]
    dateOfLatestEntry = findLatestEntry()
    day = dateOfLatestEntry + datetime.timedelta(days=1)
    while day <= datetime.date.today():
        if not isWeekend(day):
            registerWork(project_id, day)
        day += datetime.timedelta(days=1)

# Find the last day that has any registred entries on it.
def findLatestEntry():
    count = 0
    while True:
        today = datetime.date.today() - datetime.timedelta(days=count)
        todayInIso = today.isoformat()
        printDots()
        url = "https://www.toggl.com/api/v8/time_entries?start_date=" + todayInIso + "T00:00:00.000Z" + "&end_date=" + todayInIso + "T23:00:00.000Z"
        r = requests.get(url, auth=(api_token, "api_token"))
        if r.json():
            print "Found an entry for " + todayInIso
            return today
        count += 1

# Register 8 ours of work on a project for a day.
def registerWork(project_id, day):
    dayInIso = day.isoformat()
    getProjectName(project_id)
    print "Registering work for " + dayInIso + " for project " + "(id: " + str(project_id) + ")"
    url = "https://www.toggl.com/api/v8/time_entries"
    data = {"time_entry":{"duration":28800,"start":dayInIso+"T07:00:00.000Z","pid":project_id,"created_with":"toggler.py"}}
    r = requests.post(url, data=json.dumps(data), auth=(api_token, "api_token"))


def getProjectName(project_id):
    url = "https://www.toggl.com/api/v8/workspaces/" + workspace_id + "/projects" 
    r = requests.get(url, auth=(api_token,"api_token"))
    for project in r.json():
        if project["id"] == project_id:
            print "same id"
        

# We don't usually work on weekends.
def isWeekend(day):
    weekend = set([5, 6])
    return day.weekday() in weekend
    
# Print some cool dots.
def printDots():
    sys.stdout.write(".")
    sys.stdout.flush()

# Program entry
commands = { "projects" : printAllProjects, "sick" : registerSickToday, "fillup" : fillUpFromToday }
try:
    command = sys.argv[1]
    commands[command]()
except (KeyError, IndexError):
    print "No such command."
except KeyboardInterrupt:
    print "Aborted."

