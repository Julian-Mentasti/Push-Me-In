import bs4 as bs
import urllib.request
import smtplib

sauce = urllib.request.urlopen('https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=MATH&course=342&section=201').read()
soup = bs.BeautifulSoup(sauce, 'lxml')


bFound = False
bFFound = False


for paragraph in soup.find_all('td'):
    if bFound == False:
        if(paragraph.text == "Total Seats Remaining:"):
            bFound = True
    elif bFound:
        number = paragraph.text
        bFound = False
        bFFound = True

if( bFFound == False):
    print("not found")
    exit()

if(number == "0"):
    print("no change detected")
    exit()

content = 'example email stuff here'
mail = smtplib.SMTP('smtp.gmail.com',587)

mail.ehlo()
mail.starttls()
mail.login('email','password')

mail.sendmail('fromemail','reciever', content)

mail.close()