> How to enable silent automatic updates for any repository?

#  what is this?
### Procedure:
Follow the steps below:

1. Install unattended-upgrade
```sudo apt-get install unattended-upgrades```

2. Discover it works only for official repos. by default. 

### Problem:
To make it work for all repos. you need to add each source to the config file manually. This might become hassle each time you install a new software on your machine. May even lead to duplicate or unwanted entries or just a mere waste of time!!!
Stackoverflow question: http://askubuntu.com/q/87849/417607

### Solution:
Run this simple code. 
# how to run this?
* Check repositories to add:
```
$ python automatic_upgrade.py 
Add repos:
"Ubuntu:xenial";
"LP-PPA-kubuntu-ppa-backports:xenial";
"LP-PPA-tuxonice:xenial";
"LP-PPA-webupd8team-sublime-text-3:xenial";

Skipping files due to not present origin or suite. Or origin being a url.:
packagecloud.io_slacktechnologies_slack_debian_dists_jessie_InRelease
tiliado.eu_nuvolaplayer_repository_deb_dists_xenial_InRelease
```

* Now edit `/etc/apt/apt.conf.d/50unattended-upgrades` to include them:
```
// Automatically upgrade packages from these (origin:archive) pairs
Unattended-Upgrade::Allowed-Origins {
	"${distro_id}:${distro_codename}-security";
	"${distro_id}:${distro_codename}-updates";
	"${distro_id}:${distro_codename}-proposed";
	"${distro_id}:${distro_codename}-backports";
  "Ubuntu:xenial";
  "LP-PPA-kubuntu-ppa-backports:xenial";
  "LP-PPA-tuxonice:xenial";
  "LP-PPA-webupd8team-sublime-text-3:xenial";
};
....
....
```
* Check to see if they are included:
``` 
$ sudo unattended-upgrade --dry-run --debug
Initial blacklisted packages: 
Initial whitelisted packages: 
Starting unattended upgrades script
Allowed origins are: ['o=Ubuntu,a=xenial-security', 'o=Ubuntu,a=xenial-updates', 'o=Ubuntu,a=xenial-proposed', 'o=Ubuntu,a=xenial-backports', 'o=Ubuntu,a=xenial', 'o=LP-PPA-kubuntu-ppa-backports,a=xenial', 'o=LP-PPA-tuxonice,a=xenial', 'o=LP-PPA-webupd8team-sublime-text-3,a=xenial']
pkgs that look like they should be upgraded: 
Fetched 0 B in 0s (0 B/s)                                                                                  
fetch.run() result: 0
blacklist: []
whitelist: []
No packages found that can be upgraded unattended and no pending auto-removals
```
