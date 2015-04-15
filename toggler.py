#!/usr/bin/env python
import requests

print "toggl.."

r = requests.get('https://www.toggl.com/api/v8/workspaces/{ID}/projects', auth=('{KEY}','api_token'))

for project in r.json():
    print project['name']
