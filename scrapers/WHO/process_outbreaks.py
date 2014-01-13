import contextlib
from urllib import urlopen
import csv
import re

#def import_diseases(db):

CKAN_URL = "https://ckan-datastore.s3.amazonaws.com/2013-12-18T19:06:54.560Z/who-outbreak-alerts.csv"

rownum = 0

outFile = open('who-outbreak-alerts-processed.csv', "wb")

with contextlib.closing(urlopen(CKAN_URL)) as raw_csv:
    reader = csv.reader(raw_csv)
    writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for year, link, news in reader:
        if rownum == 0:
            fields_out = ['year','link', 'date', 'year2', 'title', 'update', 'body', 'news']
            writer.writerow(fields_out)
            rownum += 1
            continue
        else: 
            update_out, date_out, year2_out, title_out, body_out = ('',)*5
            if int(year) < 2012:
                update = re.search(r'[Uu]pdate\s\d{0,2}', news)
                if update:
                    #print 'Update:' + update.group()
                    update_out = update.group()
            if int(year) == 2003:
                if link == 'http://www.who.int/csr/don/2003_06_16/en/index.html':
                    date_out = '16 June 2003'
                elif link == 'http://www.who.int/csr/don/2003_07_05/en/index.html':
                    date_out = '5 July 2003'
                elif link == 'http://www.who.int/csr/don/2003_06_24/en/index.html':
                    date_out = '24 June 2003'
                else:
                    date = re.search(r'((?<=\s\s\s)(\d{1,2}.*?\d\d\d\d)(?=\s))', news)
                    if date:
                        date_out = date.group()
                        #date_out = date_tmp[0:12]
                        print 'Date:' + date.group()
            else:
                date = re.search(r'(?<=\s\s\s)(\d{1,2}.*?\d{2,4})((?=\s\-)|(?=\s\d)|(?=\sDisease)|(?=\sWith)|(?=\sSince)|(?=\sNote)|(?=\s\s\sWHO)|(?=\s\s))', news)
                if date:
                    print 'Date:' + date.group()
                    date_out = date.group()
            if int(year) < 2003:
                year2 = re.search(r'^\s\d{4}', news)
                if year2:
                    #print 'Year2:' + year2.group()
                    year2_out = year2.group()
                title = re.search(r'(?<=\-\s)(.*?)((?=\s\-)|(\s\s\s))', news)
                if title:
                    #print 'Title: ' + title.group()
                    title_out = title.group()
            else:
                title = re.search(r'^(.*?)((?=\s\-)|(\s\s\s))',news)
                if title:
                    #print 'Title: ' + title.group()
                    title_out = title.group()
            if int(year) < 2004:
                body = re.search(r'(?<=Reported\s\s)(.*?)$', news)
                if body:
                    #print 'Body: ' + body.group()
                    body_out = body.group()
            elif int(year) > 2003 and int(year) < 2009:
                body = re.search(r'(?<=\d\d\s\s\s)(.*?)$',news)
                if body:
                    #print 'Body: ' + body.group()  
                    body_out = body.group()
            else:
                body = re.search(r'(?<=\d\d\s-\s\s)(.*?)$',news)
                if body:
                    #print 'Body: ' + body.group()
                    body_out = body.group()
            rownum += 1
            content = [year,link, date_out, year2_out, title_out, update_out, body_out, news]
            writer.writerow(content)

    print rownum




