# using feedparser to get title, link, etc. of podcasts from xml rss feed
#

import feedparser
import time
import os
from mutagen.easyid3 import EasyID3

#-------------------------------------------------------------------------------------------
def getCurrentFileName(entriesGuid): # ...because we have to extract filename from entriesGuid string!
    fileName = d.entries[i].guid
    backslashPos = -1 ; idx = -1
    for lettBS in fileName :
        idx = idx + 1
        if lettBS == '/' :
            backslashPos = idx
    # now we slice fileName
    fileName = fileName[backslashPos+1:]
    print ("\t" + lettBS + " - " + str(backslashPos+1) + "\tFile name : " + fileName + "")
    return fileName
#------------------------------------------------------------------------------------------- 
def isFileAccessible(filepath, mode): # Check if a file exists and is accessible.     
    try:
        print("\t...Checking access to '" + filepath + "'... ")
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False
 
    return True
#-------------------------------------------------------------------------------------------
def getEmissionDateFromGUID(entriesGuid,fileName): # get emission date from d.entries[i].guid) <pubDate>Thu, 30 Nov 2017 11:35:00 +0100</pubDate>
    startPosition = entriesGuid.find(fileName) # get position inside the string
    dd=(entriesGuid[startPosition - 3 : startPosition - 1]) # get two chars    
    mm=(entriesGuid[startPosition - 6 : startPosition - 4]) # get two chars
    yyyy=(entriesGuid[startPosition - 11 : startPosition - 7]) # get four chars    
    emissionDate = (yyyy + "." + mm + "." + dd)
    return emissionDate
#-------------------------------------------------------------------------------------------
def getEmissionDate(entriesPublished): # get emission date from entries[i].published) <pubDate>Thu, 30 Nov 2017 11:35:00 +0100</pubDate>
    startPosition = 5 # get position inside the string
    dd=(entriesPublished[startPosition : 7]) # get two chars    
    mm=getMonthNumber(entriesPublished[8 : 11]) # get two chars
    yyyy=(entriesPublished[12 : 16]) # get four chars    
    emissionDate = (yyyy + "." + mm + "." + dd) # e.g.: 2017.11.30
    return emissionDate
#-------------------------------------------------------------------------------------------
def getMonthNumber(monthName): # returns month number got from month short name (e.g. 01 from Jan,..., 09 from Sep,... etc.)
    return {
        "Jan" : "01",
        "Feb" : "02",
        "Mar" : "03",
        "Apr" : "04",
        "May" : "05",
        "Jun" : "06",
        "Jul" : "07",
        "Aug" : "08",
        "Sep" : "09",
        "Oct" : "10",            
        "Nov" : "11",
        "Dec" : "12"
    }.get(monthName, "Invalid month (" + monthName + ")")
#-------------------------------------------------------------------------------------------
def updateID3tags(mp3FileName, title, artist, album): #from mutagen.easyid3 import EasyID3  
    # pip install mutagen  
    audio = EasyID3(mp3FileName)    #("example.mp3")
    audio['title'] = title          #u"Example Title"
    audio['artist'] = artist        #u"Me"
    audio['album'] = album          #u"My album"
    audio['composer'] = u"" # clear
    audio.save()
    print(" ... " + mp3FileName + " file successfully updated !!")
    return True
#-------------------------------------------------------------------------------------------

#===========================================================================================
#    STARTING...
#===========================================================================================
print ("\n------------------------------------------------")
print (" " + time.ctime() + " - Starting 'Feedparser test'...")
print ("------------------------------------------------\n")

d = feedparser.parse('https://www.rsi.ch/rete-due/programmi/cultura/il-giardino-di-albert/?f=podcast-xml')
parentFolder = ("E:\Podcasts\Temp") # ("S:\Podcasts\Temp\\")
podcastName = "Il_Giardino_di_Albert_"
feedTitle = d.feed.title ; entriesNr = d.entries.__len__()
currentFolder = parentFolder + "\\" + feedTitle
print ("Feed title (i.e. folder name) : " + feedTitle + " (entries : " + str(entriesNr) + ")")
print (". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
for i in range(0,entriesNr) :
    print ("\tEntries title : " + d.entries[i].title + "\n\tEntries link : " + d.entries[i].link + "\n\tEntries guid : " + d.entries[i].guid + "\n\tEntries pub date : " + d.entries[i].published)   
    currentFileName = getCurrentFileName(d.entries[i].guid) # we have to extract filename from this string
    if isFileAccessible(currentFolder + "\\" + currentFileName, 'r'):
        #emissionDate = getEmissionDate(d.entries[i].guid,currentFileName)
        emissionDate = getEmissionDate(d.entries[i].published)
        print ("\tFile '" + currentFolder + "\\" + currentFileName + "' found ! Emission date : " + emissionDate ) # build pubDate (in this format yyyy.mm.dd)		
        newFileName = podcastName + emissionDate + ".mp3" # build newFileName (as podcastName_yyyy.mm.dd.mp3)
        print ("\tnewFileName : " + newFileName + " - current working directory : " + os.getcwd())

        #... we need to check if currentFolder + "\\" + newFileName does already exist before trying to rename current file name !!
        #os.rename(currentFolder + "\\" + currentFileName, currentFolder + "\\" + newFileName) # update currentFileName with newFileName
        #in case it does exist we can simply append "_" + currentFileName in order to avoid duplicate filenames !!
        # also we need to get effective functions and subroutines instead of repeating code lines....

        os.rename(currentFolder + "\\" + currentFileName, currentFolder + "\\" + newFileName) # update currentFileName with newFileName
        # update <<Title>> ID3tag, just assigning <<d.entries[i].title>> string
        updateID3tags(currentFolder + "\\" + newFileName, d.entries[i].title, "", "")
        print ("\n\n")
    else :
        print ("\tFile '" + currentFolder + "\\" + currentFileName + "' is not accessible !!\n")  

print ("\n------------------------------------------------------------------------------------------------\n")

d = feedparser.parse('https://www.rsi.ch/rete-due/programmi/cultura/birdland/?f=podcast-xml')
#currentFolder = ('E:\Podcasts\Temp')
podcastName = "Birdland_"
feedTitle = d.feed.title ; entriesNr = d.entries.__len__()
currentFolder = parentFolder + "\\" + feedTitle
print ("Feed title (i.e. folder name) : " + feedTitle + " (entries : " + str(entriesNr) + ")")
print (". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
for i in range(0,entriesNr) :
    print ("\tEntries title : " + d.entries[i].title + "\n\tEntries link : " + d.entries[i].link + "\n\tEntries guid : " + d.entries[i].guid + "\n\tEntries pub date : " + d.entries[i].published)
    currentFileName = getCurrentFileName(d.entries[i].guid) # we have to extract filename from this string
    if isFileAccessible(currentFolder + "\\" + currentFileName, 'r'):
        #emissionDate = getEmissionDate(d.entries[i].guid,currentFileName)
        emissionDate = getEmissionDate(d.entries[i].published)
        print ("\tFile '" + currentFolder + "\\" + currentFileName + "' found ! Emission date : " + emissionDate ) # build pubDate (in this format yyyy.mm.dd)		
        newFileName = podcastName + emissionDate + ".mp3" # build newFileName (as podcastName_yyyy.mm.dd.mp3)
        print ("\tnewFileName : " + newFileName + " - current working directory : " + os.getcwd())
        os.rename(currentFolder + "\\" + currentFileName, currentFolder + "\\" + newFileName) # update currentFileName with newFileName
        # update <<Title>> ID3tag, just assigning <<d.entries[i].title>> string
        updateID3tags(currentFolder + "\\" + newFileName, d.entries[i].title, "", "")
        print ("\n\n")
    else :
        print ("\tFile '" + currentFolder + "\\" + currentFileName + "' is not accessible !!\n") 

print ("\n------------------------------------------------------------------------------------------------\n")

d = feedparser.parse('http://www.rsi.ch/rete-tre/programmi/intrattenimento/il-disinformatico/?f=podcast-xml')
#currentFolder = ('S:\Podcasts\Temp')
podcastName = "Il_Disinformatico_"
feedTitle = d.feed.title ; entriesNr = d.entries.__len__()
currentFolder = parentFolder + "\\" + feedTitle
print ("Feed title (i.e. folder name) : " + feedTitle + " (entries : " + str(entriesNr) + ")")
print (". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
for i in range(0,entriesNr) :
    print ("\tEntries title : " + d.entries[i].title + "\n\tEntries link : " + d.entries[i].link + "\n\tEntries guid : " + d.entries[i].guid + "\n\tEntries pub date : " + d.entries[i].published)
    currentFileName = getCurrentFileName(d.entries[i].guid) # we have to extract filename from this string
    if isFileAccessible(currentFolder + "\\" + currentFileName, 'r'):
        #emissionDate = getEmissionDate(d.entries[i].guid,currentFileName)
        emissionDate = getEmissionDate(d.entries[i].published)
        print ("\tFile '" + currentFolder + "\\" + currentFileName + "' found ! Emission date : " + emissionDate ) # build pubDate (in this format yyyy.mm.dd)		
        newFileName = podcastName + emissionDate + ".mp3" # build newFileName (as podcastName_yyyy.mm.dd.mp3)
        print ("\tnewFileName : " + newFileName + " - current working directory : " + os.getcwd())
        os.rename(currentFolder + "\\" + currentFileName, currentFolder + "\\" + newFileName) # update currentFileName with newFileName
        # update <<Title>> ID3tag, just assigning <<d.entries[i].title>> string
        updateID3tags(currentFolder + "\\" + newFileName, d.entries[i].title, "", "")
        print ("\n\n")

print ("\n------------------------------------------------------------------------------------------------\n")

prices = {'apple': 0.40, 'banana': 0.50}
my_purchase = {
    'apple': 1,
    'banana': 6}
grocery_bill = sum(prices[fruit] * my_purchase[fruit]
                   for fruit in my_purchase)
print ('\nI owe the grocer $%.2f' % grocery_bill)