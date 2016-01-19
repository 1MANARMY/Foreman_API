# Foreman_API
Description: Foreman API can be tricky if you are not well versed in the subject of a Restful API Library.

Language: Python

Requirements:
- Requests
- Foreman API to pull from
- Elbow Grease

Install: 

$ pip install requests

OR

Get the code from git://github.com/kennethreitz.git and then just $ python setup.pr install to make it official


More Info @ docs.python-requests.org/en/latest/

Using:

My script was designed to run on Linux based systems. Tested on centos6.5, centos7, fedora23 and Ubuntu14.02 (not 15).

- Foreman API Puller:
     Available flags::                  
    -o out of sync hosts              
    -n non production hosts           
    -t hosts with changes made today  
    -f hosts in foreman, not in secondary pool  
    -b hosts in foreman in build mode 
    ./script -n' will display out of sync hosts

Enjoy
