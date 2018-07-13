# @dotSlashJack
# NYT Book Review Web Parser, easily adaptable to other websites
# Note: depends on beautifulsoup4, and urllib2!
import datetime as dt
import urllib2
import time
from bs4 import BeautifulSoup as bs
import os.path
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
reload(sys)
sys.setdefaultencoding('utf8')


# configuring a set of dates to place in URLs to download from
nWeeks = 300 # number of weeks back to go
#nWeeks = sys.argv[0]
#print('Going back '+ str(nWeeks) + ' weeks.')
today = dt.date(2018, 7, 15) #set starting date (must correspond with NYT week)
dayMinus = 7
base_yr, base_mo, base_day = str(today.year), str(today.month), str(today.day)
if len(base_mo)==1:
    base_mo = '0'+base_mo
if len(base_day)==1:
    base_day = '0'+base_day
todayStr = base_yr+'/'+base_mo+'/'+base_day
reviewDates = [todayStr]


# Generating a list of times to place in URLs to check
for i in range(1, nWeeks+1):
    nDate = today - dt.timedelta(days=dayMinus)
    yr, mo, day = str(nDate.year), str(nDate.month), str(nDate.day)
    if len(mo)==1:
        mo = '0'+mo
    if len(day)==1:
        day = '0'+day
    dateStr = yr+'/'+mo+'/'+day
    reviewDates.append(dateStr)
    dayMinus += 7



# Generating a list of URLs to check for download links
baseURL = 'https://www.nytimes.com/books/best-sellers/'
urls = []
for i in range(0, nWeeks):
    urls.append(baseURL+reviewDates[i]+'/combined-print-and-e-book-fiction/')
print('Finished setting weeks (back) to check.')

dlList = [] # list of actual urls to download
currLink = '' # current link in page to download
currURL = '' # (selected) url of each week of book reviews
for i in range(0, nWeeks):
    currURL = urls[i]
    if i>0 and i%30==0:
        print('Paused to prevent server overload')
        time.sleep(20) # prevent server request overload
        print('Resumed')
    sauce = urllib2.urlopen(currURL).read()
    soup = bs(sauce)
    for a in soup.find_all('a', href=True, class_='review-link'):
        currLink = a['href']
        if currLink not in dlList:
            dlList.append(currLink)

print('Finished collecting article urls.')
#print(dlList)

# get the title
def title(currSoup):
    try:
        dateString = currSoup.time['datetime'] # got time from the article's html
        dateString = dateString.split('T')[0]
    except(TypeError, KeyError) as e:
        dateString='0001-01-01'
        pass
    #bookTitle = currSoup.find('strong', class_='css-8qgvsz euv7paa0').string
    #bookTitle = bookTitle.replace(' ','-') # replace spaces with dashes for easy ngrams use
    articleTitle = currSoup.find('title').string
    articleTitle = articleTitle.replace('- The New York Times','')
    articleTitle = articleTitle.replace(' ','-')
    articleTitle = articleTitle.replace('/','')
    #author = currSoup.find('p', class_='css-1i0edl6 e2kc3sl0').contents[3] # get the authors
    #author = author.replace('By ','')# remove 'by' to leave author names
    #author = author.replace(' ','-')

    #titleStr = author+articleTitle+','+dateString+'.txt' # ngram friendly file name
    titleStr = articleTitle+','+dateString # ngram friendly file name
    titleStr = titleStr.replace('/','')
    return titleStr

# download the text, put in file
def download(currSoup, file):
    try:
        for p in currSoup.find_all('p', class_='css-1i0edl6 e2kc3sl0')[1:]:
            text = p.text
            file.write(str(text)+'\n')
    except(TypeError, KeyError) as e:
        try:
            for p in currSoup.find_all('p', class_='story-body-text story-content')[1:]:
                file.write(str(text)+'\n')
                text = p.text
        except(TypeError, KeyError) as e:
            print('ERROR: No text found for: ')
            print(currSoup)
            print('---')
            pass

# main loop, writes files for all of the reviews
length = int(len(dlList)) # number of the sublinks (articles) to download
print('Downloading articles and generating files, this may take a while!\n')
for i in range(0, length):
    sauceDL = urllib2.urlopen(dlList[i]).read()
    if i>0 and i%40==0:
        print('Paused to prevent server overload')
        time.sleep(30) # prevent server request overload
        print('Resumed')
    print(dlList[i])
    soupDL = bs(sauceDL)
    #print(dlList[i])
    titleStr = title(soupDL)
    save_path = '/Users/jhester/Box Sync/Fall 2018 LING 499R-NLP/NYTExtraction'
    titleComplete = os.path.join(save_path, titleStr+'.txt')
    f = open(titleComplete,'w+')
    download(soupDL, f)
    f.close()

    complete = (i*100.0)/length
    sys.stdout.flush()
    sys.stdout.write(str(complete) + '% complete ')

print(str(length) + 'files outputted')
print('\nComplete, check output folder!')
