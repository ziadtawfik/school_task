import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

schoollink = []
schoolname = []
headofschool = []
emailadress = []
phonenumber = []
counter = 0

def revese(s):
    stringlength=len(s)
    slicedString=s[stringlength::-1]
    return slicedString

#getting url & content
url = ('https://www.nysais.org/page.cfm?p=1082')
data = requests.get(url)
cdata = data.content
#cdata
#soup object
allsoup = BeautifulSoup(cdata,'lxml')
soup = allsoup.find('ul',{"class":"sitemap_list text_misc"})

soup
#get wanted data
schoollinks = soup.find_all('a')
for i in range(len(schoollinks)):
  x=schoollinks[i].get('href')
  schoollink.append(f'https://www.nysais.org/{x}')
schoollink=schoollink[:-2]

def gettingschoolinfo(url):
    data = requests.get(url)
    cdata = data.content
    cdata
    soupallpage = BeautifulSoup(cdata,'lxml')
    soup = soupallpage.find('table',{'cellpadding':'2'})
    soup
    schoolname11 = soup.find_all('h1')
    scname=schoolname11[0].text
    elrageleltama = soup.find('div',{'class':'profileContactItem'})
    headname = elrageleltama.findAll('a',{'href':'javascript:void(0);'})
    scheadname=headname[1].text.strip()
    scnum=soup.find('td',{'class':'datatitle'},text='Phone')
    if scnum != None:
        scnum = scnum.find_next_sibling().text
    else:
        scnum = 'notfound '    
    headschoolprpfile = soup.find_all('div',{'class':'profileContactItem'})
    headschoolprpfile[0]
    headschoolprpfilelink = headschoolprpfile[0].find_all('a')[1].attrs.get('onclick')
    headschoolprpfilelink=str(headschoolprpfilelink)
    headschoolprpfilelink = headschoolprpfilelink[7:headschoolprpfilelink.find(',')-1]
    headschoolprpfilelink
    headschoolprpfilelinkdata = requests.get(f'https://www.nysais.org/{headschoolprpfilelink}')
    hdsclinkcdata = headschoolprpfilelinkdata.content
    hdsclinkallpage = BeautifulSoup(hdsclinkcdata)
    email = hdsclinkallpage.find('div',{'id':'sectionContactInformation'})
    if email == None:
        email = hdsclinkallpage.find('div',{'id':'sectionContactInfo'})
    if email != None:
        if email != 'None':
            email = email.find('div',{'class':'profileFieldValue'}).script
            if email != None:
                email = str(email)
                email = email[email.find('(')+2:email.find(')')-1]
                firstlink = email.split(',')[0].strip()[:-1]
                lastlink = email.split(',')[1].strip()[1::]
                hdemail=f'{revese(lastlink)}@{revese(firstlink)}'
            else:
                hdemail='not found '
        else:
            hdemail='not found '
    else:
        hdemail='not found '
    print(scname,scheadname,scnum,hdemail)
    schoolname.append(scname)
    headofschool.append(scheadname)
    emailadress.append(hdemail)
    phonenumber.append(scnum)

for t in schoollink:
    print('we are in the school number: ',counter)
    counter+=1
    print(t)
    gettingschoolinfo(t)

print(schoolname,headofschool, emailadress,phonenumber)
print(schoolname.__len__(),headofschool.__len__(), emailadress.__len__(),phonenumber.__len__())

x = zip_longest(schoolname , headofschool , emailadress , phonenumber , schoollink)
with open ("/home/itageldin/Documents/schools.csv","w") as school:
    wr = csv.writer(school)
    wr.writerow(['school name' , 'head of school name' , 'email adress of head of the school' , 'school phone number' , 'school information link'])
    wr.writerows(x)