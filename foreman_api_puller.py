#!/usr/bin/env python

import sys
import json
import requests

def main(argv):
  # Authentication information to pass into requests
  usr = <Enter a user name>
  pswd = <Enter password>

  # API url to get request from
  # Note: we're using the hosts from the API, link may
  #       differ based on what the requested data is
  #  Example: https://foreman.network.com/api/v2/hosts
  # /hosts would would change based on data
  foreman_url = <Enter your URL for Foreman>
  sec_pool_url = <Enter your URl for secondary pool>
  # Warnings disabled so when piping stdout to a file we
  # don't get unwanted warnings, which might cause problems
  # with further log parsing
  requests.packages.urllib3.disable_warnings()

  flag = sys.argv[1]
  if flag == '-o':
    # Using requests library to make a GET with given api url and auth
    # Note: Verify is set to false 
    # Payload is the search string, in this case for out of sync nodes
    # Note: the query string has to be EXACT, included spaces.
    #       e.g. last_report<"2 hours ago" is not the same as 
    #            last_report < "2 hours ago"
    payload = {'search':'last_report < "2 hours ago"'}
    #change the timing to what you see fit
    r = requests.get(foreman_url, auth=(usr, pswd), verify=False, params=payload)
    # Iterate through every object in results and print the hostname and ip
    # Note: Some IP's are set to None, hence the use of str() to avoid type
    # errors when encountering any IP's that are set to None.
    for obj in json.loads(r.text)['results']:
      print "Hostname: " + str(obj['name']) + ", IP: " + str(obj['ip'])
  elif flag == '-n':
    # No parameters for this request, will iterate through all results to
    # return only non production nodes
    r = requests.get(foreman_url, auth=(usr, pswd), verify=False)
    for obj in json.loads(r.text)['results']:
      if obj['environment_name'] != 'production':
        print "Hostname: " + str(obj['name']) + ", IP: " + str(obj['ip'])
  elif flag == '-t':
    # Getting nodes updated today
    payload = {'search':'last_report = Today'}
    r = requests.get(foreman_url, auth=(usr, pswd), verify=False, params=payload)
    for obj in json.loads(r.text)['results']:
      print "Hostname: " + str(obj['name']) + ", IP: " + str(obj['ip'])
  elif flag == '-f':
    # Comparing nodes between foreman and another restful api
    sec_pool_r = requests.get(sec_pool_url)
    foreman_r = requests.get(foreman_url, auth=(usr, pswd), verify=False)
    host_dict = {}

    for obj in json.loads(foreman_r.text)['results']:
      hostname = str(obj['name']).split('.')[0]
      ip = str(obj['ip'])
      host_dict[hostname] = (ip, False)

    for obj in json.loads(sec_pool_r.text):
      hostname = str(obj['host_name'])
      if hostname in host_dict:
        host_dict[hostname] = (host_dict[hostname][0],True)

    for key, value in host_dict.iteritems():
      if value[1] == False:
        print "Hostname: " + key + ", IP: " + str(value[0])
  elif flag == '-b':
    r = requests.get(foreman_url, auth=(usr, pswd), verify=False)
    for obj in json.loads(r.text)['results']:
      if str(obj['build']).lower() == 'true':
        print "Hostname: " + str(obj['name']) + ", IP: " + str(obj['ip'])
  else:
    print " Available flags:                  "
    print " -o out of sync hosts              "
    print " -n non production hosts           "
    print " -t hosts with changes made today  "
    print " -f hosts in foreman, not in ship  "
    print " -b hosts in foreman in build mode "
    print " e.g.: './script -n' will display out of sync hosts."

if __name__ == "__main__":
  main(sys.argv[1:])
