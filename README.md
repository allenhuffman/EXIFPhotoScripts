# EXIF Photo Scripts

Various scripts (shell, python) I have been working on to do useful (to me) things with digital camera photos.

## showdatesinphotos.sh
Recurses through folders and shows the unique dates photos were taken. I wrote this so I could go through my library of hundreds of thousands of vacation photos and see what dates I was on trips.

## showphotoswithoutdates.sh
My older camera did not have EXIF yet and, instead, used JFIF data. Back then, photo tools did not yet know how to deal with this, so if I edited the photo in any way, such as to rotate it, it would lose the header date code information. This tool helps me find photos that do not have embedded date code. In the future, I am going to make it rename them to have "_notime" or something at the end, so I can know not to try to rename them using EXIF date code (since that does not work).

## showuniquefocallengths.py
After looking at a camera that had manual zoom, I wondered if I'd miss that if I didn't have it. I had this script written to show me the percentage of zooms (focal lenghts) in the photos I take. One visit to Disneyland shows me using no zoom 84% of the time, meaning I use zoom for 16% of my photos. Having to manually zoom would be something I'd be doing more than one out of ten photos I take. I probably will not be getting a manual zoom camera any time soon.

More to come...
