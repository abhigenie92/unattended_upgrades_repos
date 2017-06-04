#!/usr/bin/env python3
import os
import re
import sys
import fileinput
import shutil
import datetime
if len(sys.argv) > 1 and sys.argv[1] == 'y':
    INVOKED = 1
    APPLYQUERY = 'y'
else:
    INVOKED = 0
STARTTIME = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
TARGETFILE = "/etc/apt/apt.conf.d/50unattended-upgrades"
## Get the repos
PATH = '/var/lib/apt/lists/'
FILES = os.listdir(PATH)
RELEASE_FILES = [file for file in FILES if file.endswith('Release')]

ORIGIN_PATTERN = re.compile('Origin: (.*)\n')
SUITE_PATTERN = re.compile('Suite: (.*)\n')
REGEX_URL = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

skipped_release_files = []
repos_to_add = []
#Determine Distro
os_info = {}
with open('/etc/os-release', 'r') as f:
    for line in f:
        if '=' in line:
            v, w = line.split('=', 1)
            os_info[v] = w
DISTRO = os_info['NAME'].replace('"', '').replace('\n', '')
CODENAME = os_info['VERSION_CODENAME'].replace('\n', '')
for release_file in RELEASE_FILES:
    with open(PATH+release_file, 'r') as f:
        read_data = f.read()
        # parse to get origin and suite
        origin_string = re.findall(ORIGIN_PATTERN, read_data)[0]
        origin_replaced = origin_string.replace(',', r'\,').replace(DISTRO, '${distro_id}')
        suite_string = re.findall(SUITE_PATTERN, read_data)[0]
        suite_replaced = suite_string.replace(',', r'\,').replace(CODENAME, '${distro_codename}')
        try:
            repo = "\"%s:%s\";" %(origin_replaced, suite_replaced)
            if re.match(REGEX_URL, origin_string):
                skipped_release_files.append(release_file)
            else:
                repos_to_add.append(repo)
        except IndexError:
            skipped_release_files.append(release_file)



## Checking if repos_to_add not already present  in /etc/apt/apt.conf.d/50unattended-upgrades

with open(TARGETFILE, 'r') as f:
    READ_DATA = f.read()
    # get everything before first };
    RAW_DATA = re.findall(r'[.\s\S]*};', READ_DATA)[0]
    REPOS_ALREADY_PRESENT = re.findall('".*:.*";', RAW_DATA)

repos_to_add = [repo for repo in repos_to_add if repo not in REPOS_ALREADY_PRESENT]
if repos_to_add:
    while 1:
        if not INVOKED:
            print("Repos to add:")
            print('\x1b[1;32;40m' + '\n'.join(repos_to_add) + '\x1b[0m')
            print("Do you want to insert these into 50unattended-upgrades? [Y/n]")
            APPLYQUERY = input().lower()
        if APPLYQUERY == '' or APPLYQUERY == 'y' or APPLYQUERY == 'yes':
            if os.geteuid() != 0:
                print("Didn't invoke as superuser.")
                print('\x1b[1;31;40m' + "Do you want to elevate priviledges? [Y/n]" + '\x1b[0m')
                UIDQUERY = input().lower()
                if UIDQUERY == '' or UIDQUERY == 'y' or UIDQUERY == 'yes':
                    os.execvp("sudo", ["sudo"] + sys.argv + ["y"])
                else:
                    print("Aborting.")
                    break
            else:
                print("Create backup of current 50unattended-upgrades file? [Y/n]")
                BACKUPQUERY = input().lower()
                if BACKUPQUERY == '' or BACKUPQUERY == 'y' or BACKUPQUERY == 'yes':
                    shutil.copy2(TARGETFILE, TARGETFILE+"-"+STARTTIME+".bak")
                for line in fileinput.FileInput(TARGETFILE, inplace=1):
                    if "Unattended-Upgrade::Allowed-Origins {" in line:
                        line = line.replace(line, line+'\n'.join(repos_to_add) + '\n')
                    print(line, end="")
                break
        elif APPLYQUERY == 'n' or APPLYQUERY == 'no':
            print("Not added.\n")
            break
        else:
            print("Please enter y/yes/CR or n/no\n")
if skipped_release_files:
    print("Skipping files due to not present origin or suite. Or origin being a url.:\n")
    print('\x1b[1;32;40m' + '\n'.join(skipped_release_files) + '\x1b[0m')
else:
    if not repos_to_add:
        print("Nothing do to.")
