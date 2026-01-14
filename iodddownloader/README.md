# Iodd Downloader

A little utility to download all the wanted distributions to my iodd 
installation device.

## How to run

Run this with 

	ansible-playbook downloader.yml

If everything goes well, there should be a folder named distros,
which contains a bunch of iso files.

	├── distros
	    ├── debian
	    ├── redhat
	    └── ubuntu
	        └── ubuntu-22.04.iso
