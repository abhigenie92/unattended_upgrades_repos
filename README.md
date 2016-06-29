# how to run
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
$ sudo unattended-upgrade --dry-run
$ tail -5 /var/log/unattended-upgrades/unattended-upgrades.log
2016-06-29 12:30:36,259 INFO Initial blacklisted packages: 
2016-06-29 12:30:36,259 INFO Initial whitelisted packages: 
2016-06-29 12:30:36,259 INFO Starting unattended upgrades script
2016-06-29 12:30:36,259 INFO Allowed origins are: ['o=Ubuntu,a=xenial-security', 'o=Ubuntu,a=xenial-updates', 'o=Ubuntu,a=xenial-proposed', 'o=Ubuntu,a=xenial-backports', 'o=Ubuntu,a=xenial', 'o=LP-PPA-kubuntu-ppa-backports,a=xenial', 'o=LP-PPA-tuxonice,a=xenial', 'o=LP-PPA-webupd8team-sublime-text-3,a=xenial']
2016-06-29 12:30:38,708 INFO No packages found that can be upgraded unattended and no pending auto-removals
```
