import json
import requests
import sys

# following repos were used for testing
#
#has issues: gespi1/github-exercise
#no issues:  gespi1/tweetyv2

repo = input("repo name (e.g.microsoft/vscode): ") # take user input interactively
resp = requests.get('https://api.github.com/repos/{}/issues'.format(repo))

if resp.status_code != 200:
  # 200 wasnt returned, meaning repo was not a valid
  # we return specific errors for different codes 404, 502, 504, etc
  if resp.status_code == 404:
    sys.exit(json.dumps({"error": "status code: {}".format(resp.status_code), "message": "repo {} was not found".format(repo)}, sort_keys=True, indent=2))
  elif resp.status_code == 502:
    sys.exit(json.dumps({"error": "status code: {}".format(resp.status_code), "message": "bad gateway, looks like github may be experienceing issues. Try again later"}, sort_keys=True, indent=2))
  elif resp.status_code == 502:
    sys.exit(json.dumps({"error": "status code: {}".format(resp.status_code), "message": "took too long to reach github, looks like github may be experienceing issues. Try again later"}, sort_keys=True, indent=2))
  else:
    sys.exit(json.dumps({"error": "status code: {}".format(resp.status_code), "message": "Unknown status code. Try again later"}, sort_keys=True, indent=2))

data = json.loads(resp.text) # load payload as json

if data: # condition is met when there are open issues
  issue_data=[]
  for item in data: # iterate through each item in the list  
    if item["state"] == "open": # we only care about open issues
      l = []
      for label in item["labels"]: # label names are in a nested list, iterate through them
        l.append(label["name"])    # append labels to a new list
      item = {
        "url": item["url"],
        "labels": l
      }
      issue_data.append(item)
  print(json.dumps(issue_data, sort_keys=True, indent=2)) # prettify json
else: # condition is met when there are no open issues
  print(json.dumps({"info": "no open issues found for {}".format(repo)}, sort_keys=True, indent=2)) # prettify json

