#!/usr/bin/env python
import requests
import ConfigParser 

# Load configs
config = ConfigParser.ConfigParser()
config.read("./conf.ini")
api_token = config.get("ConfigSection", "api_token")
workspace_id= config.get("ConfigSection", "workspace_id")


def printAllProjects():
    r = requests.get("https://www.toggl.com/api/v8/workspaces/" + workspace_id + "/projects", auth=(api_token,"api_token"))
    for project in r.json():
        print "#  " + str(project["id"]) + "  #  " + project["name"]

printAllProjects()
