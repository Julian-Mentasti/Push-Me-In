import bs4 as bs
import urllib.request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

sUrl = 'edit'
sFrom = 'edit'
sTo = 'edit'
password = 'edit'


sauce = urllib.request.urlopen(sUrl).read()
soup = bs.BeautifulSoup(sauce, 'lxml')


bFound = False
bFFound = False


for paragraph in soup.find_all('td'):
    if bFound == False:
        if paragraph.text == "Total Seats Remaining:":
            bFound = True
    elif bFound:
        number = paragraph.text
        bFound = False
        bFFound = True

if( bFFound == False):
    print("not found")
    exit()
    #TODO ADD ERROR HANDLING

if(number == "0"):
    print("no change detected")
    exit()
    # TODO ADD ERROR HANDLING


reTitle = soup.title.text
reRegex = r'([^-]+)-{1}'
sTitle = re.findall(reRegex, reTitle)[0] + "-" + re.findall(reRegex, reTitle)[1] + "- THERE IS A FREE SEAT!"
print(sTitle)



msg = MIMEMultipart()
msg['From'] = sFrom
msg['To'] = sTo
msg['Subject'] = sTitle

body = "<a href="+ sUrl+ "> Log in now!</a> There are " + number + " seats remaining. About time you were pushed in!"


msg.attach(MIMEText(body, 'html'))
print(msg)

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(msg['From'],password)
server.sendmail(msg['From'],msg['To'], msg.as_string())
server.quit()

#garb under this

#obody = "<table> \n " \
#         "   <tr> \n " \
#         "       <td align="center"><img src="logo.jpg"></td>
#
#         </tr>
#
#         <tr>
#
#                <td>Content</td>
#
#         </tr>
#
#         <tr>
#
#                <td align="center">123 Main St. Nashville, TN 37212</td>
#
#         </tr>
#
# </table>"