import time
from time import gmtime, strftime
import pandas
import bs4 as bs
import urllib.request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import threading
import sys

starttime=time.time()

data = pandas.read_csv("classes-url.csv")
urls = list(data.Url)

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)


def checkClass(sUrl):
    output = lookUp(sUrl)
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    file = open('log.txt','a')
    file.write(date + ": " + output + '\n')

    if(len(output) > 20):
        global urls
        urls.remove(sUrl)
        print("removed: " + sUrl)

#----

def lookUp(url):
    sUrl = url
    sFrom = 'editme'
    sTo = 'editme'
    password = 'editme'

    sauce = urllib.request.urlopen(sUrl).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')

    bFound = False
    bFFound = False


    for paragraph in soup.find_all('td'):
        if bFound == False:
            if paragraph.text == "General Seats Remaining:":
                bFound = True
        elif bFound:
            number = paragraph.text
            bFound = False
            bFFound = True

    if( bFFound == False):
        return("not found")

    if(number == "0"):
        return("no change detected")

    reTitle = soup.title.text
    reRegex = r'([^-]+)-{1}'
    sTitle = re.findall(reRegex, reTitle)[0] + "-" + re.findall(reRegex, reTitle)[1] + "- THERE IS A FREE SEAT!"

    msg = MIMEMultipart()
    msg['From'] = sFrom
    msg['To'] = sTo
    msg['Subject'] = sTitle

    body = "<a href="+ sUrl+ "> Log in now!</a> There are " + number + " seats remaining. About time you were pushed in!"


    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(msg['From'],password)
    server.sendmail(msg['From'],msg['To'], msg.as_string())
    server.quit()

    return("A seat was found! for " + sTitle)
#----

spinner = Spinner()
spinner.start()
while True:
    for url in urls:
        checkClass(url)

    if len(urls) == 0:
        spinner.stop()
        exit()
    time.sleep(120.0 - ((time.time() - starttime) % 60.0))



