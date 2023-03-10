#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# load info.plist into a variable while maintaining newlines
timestamp=`date +%s`
newInfo=`echo "$(cat Version-Spy.roboFontExt/info.plist)" | sed -Ee "s/<real>([0-9]+\.*[0-9]*)/<real>$timestamp.0/g"`
echo "$newInfo" > Version-Spy.roboFontExt/info.plist

git add -- Version-Spy.roboFontExt/info.plist

PART=${1-patch}

bump2version $PART

git push 
git push --tags