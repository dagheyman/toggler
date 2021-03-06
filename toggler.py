#!/usr/bin/env python

import requests
import configparser 
import sys
import json
import datetime
import os

# Set encoding for std.out
os.environ["PYTHONIOENCODING"] = "utf-8"

# Load configs
config = configparser.ConfigParser()
config.read("./conf.ini")
api_token = config.get("ConfigSection", "api_token")
workspace_id = config.get("ConfigSection", "workspace_id")
sick_project_id = config.get("ConfigSection", "sick_project_id")

# Prints all available workspaces
def printWorkspaces():
    url = "https://www.toggl.com/api/v8/workspaces"
    r = requests.get(url, auth=(api_token, "api_token"))
    handleErrors(r.status_code)
    for workspace in r.json():
        print (str(workspace["id"]) + " - " + workspace["name"])

# Prints all the projects and id's for the current workspace.
def printAllProjects():
    url = "https://www.toggl.com/api/v8/workspaces/" + workspace_id + "/projects" 
    r = requests.get(url, auth=(api_token,"api_token"))
    handleErrors(r.status_code)
    for project in r.json():
        print (str(project["id"]) + "  -  " + project["name"])

# Registers 8 hours of sickness for today on the predefined sick-project.
def registerSickToday():
    url = "https://www.toggl.com/api/v8/time_entries"
    today = datetime.date.today().isoformat()
    data = {"time_entry":{"duration":28800,"start":today+"T07:00:00.000Z","pid":sick_project_id,"created_with":"toggler.py"}}
    r = requests.post(url, data=json.dumps(data), auth=(api_token, "api_token"))
    print ("Registered sick today.")

# Register work for all empty days until today, using the first argument as project id.
def fillUpFromToday():
    project_id = sys.argv[2]
    dateOfLatestEntry = findLatestEntry()
    day = dateOfLatestEntry + datetime.timedelta(days=1)
    while day <= datetime.date.today():
        printDots()
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
            return today
        count += 1

# Register 8 ours of work on a project for a day.
def registerWork(project_id, day):
    dayInIso = day.isoformat()
    url = "https://www.toggl.com/api/v8/time_entries"
    data = {"time_entry":{"duration":28800,"start":dayInIso+"T07:00:00.000Z","pid":project_id,"created_with":"toggler.py"}}
    r = requests.post(url, data=json.dumps(data), auth=(api_token, "api_token"))
    handleErrors(r.status_code)

# We don't usually work on weekends.
def isWeekend(day):
    weekend = set([5, 6])
    return day.weekday() in weekend
    
# Print some cool dots.
def printDots():
    sys.stdout.write(".")
    sys.stdout.flush()

# Handle error codes from API.
def handleErrors(status_code):
    if status_code == 400:
        print ("Something went wrong.")
        sys.exit(1)
    if status_code == 403:
        print ("Toggl refuses the request. Do you have the correct API token?")
        sys.exit(1)

# Program entry
commands = { "workspaces": printWorkspaces, "projects" : printAllProjects, "sick" : registerSickToday, "fillup" : fillUpFromToday }
try:
    command = sys.argv[1]
    commands[command]()
except (KeyError, IndexError):
    print ("No such command.")
except KeyboardInterrupt:
    print ("Aborted.")
except ValueError:
    print ("Something went wrong.")
