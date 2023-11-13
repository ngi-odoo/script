#!/bin/bash
if [ "$1" == "master" ] || [ "$1" == "10" ] || [ "$1" == "11" ] || [ "$1" == "12" ] || [ "$1" == "13" ] || [ "$1" == "14" ] || [ "$1" == "15" ] || [ "$1" == "16" ] || [ "$1" == "17" ]; then
	if [ "$1" == "master" ]; then
		VERSION=${1}
	else
		VERSION=${1}.0
	fi
	echo "Version: ${VERSION}"
	cd ~/Desktop/Dev/Python/odoo
	git add .
	git reset --hard
	git checkout $VERSION
	git pull origin $VERSION
	cd ~/Desktop/Dev/Python/enterprise
	git add .
	git reset --hard
	git checkout $VERSION
	git pull origin $VERSION
	echo "Done !"
else
	echo "Wrong version. Please enter master, 10, 11, 12, 13, 14, 15, 16 or 17"
fi
