import os,re,pdb
from pprint import pprint
## Get the repos
path='/var/lib/apt/lists/'
files=os.listdir(path)
release_files=[file for file in files if file.endswith('Release')]

origin_pattern=re.compile('Origin: (.*)\n')
suite_pattern=re.compile('Suite: (.*)\n')
regex_url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

skipped_release_files=[]
repos_to_add=[]
for release_file in release_files:
  with open(path+release_file, 'r') as f:
    read_data = f.read()
    # parse to get origin and suite
    origin_string=re.findall(origin_pattern,read_data)
    suite_string=re.findall(suite_pattern,read_data)
    try:
      repo="\"%s:%s\";" %(origin_string[0].replace(',',r'\,'),
                            suite_string[0].replace(',',r'\,'))
      if re.match(regex_url,origin_string[0]):
        skipped_release_files.append(release_file)
      else:
        repos_to_add.append(repo)
    except IndexError:
      skipped_release_files.append(release_file)



## Checking if repos_to_add not already present  in /etc/apt/apt.conf.d/50unattended-upgrades

with open('/etc/apt/apt.conf.d/50unattended-upgrades','r') as f:
  read_data=f.read()
  # get everything before first };
  raw_data=re.findall('[.\s\S]*};',read_data)
  repos_already_present=re.findall('".*:.*";',raw_data[0])

repos_to_add=[repo for repo in repos_to_add if repo not in repos_already_present]
print ("Add repos:")
print ('\n'.join(repos_to_add))
print ("\nSkipping files due to not present origin or suite. Or origin being a url.:")
print ('\n'.join(skipped_release_files))
