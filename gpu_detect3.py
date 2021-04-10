import requests
from bs4 import BeautifulSoup
import smtplib
import time

headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}


def check_price(trig, link, iddd, nev, max_ar):
	
	page = requests.get(link, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	# Ar, es annak atalakitasa
	price = 0
	if trig == "altex.ro":
		price = soup.find('span',{'class':'Price-int'}).get_text()
	if trig == "cel.ro":
		price = soup.find(id=idd).get_text()
	if trig == "itgalaxy.ro":
		ar1 = soup.find(itemprop="price").get_text()
		ures_nelkuli = ar1.lstrip('\n')
		price = ures_nelkuli[0:5]
	if trig == "evomag.ro":
		ar1 = soup.find("div",{"class": "pret_rons"}).get_text()
		price = ar1[0:5]

	# Az atalakitasnal a pont bezavarja ezert ezt replacelem
	nativ_ar = price.replace('.','')
	converted_price = float(nativ_ar)

	# Uzenet kepzes
	subject = 'Price fell down on {}!'.format(nev.upper())
	body = 'New price: {} RON, check the link: {}'.format(converted_price, link)
	msg = 'Subject: {}\n\n{}'.format(subject, body)

	# Ellenorzes, majd email kuldes a megfelelo uzenettel
	if(converted_price < max_ar):
		send_mail(msg)


def send_mail(msg):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login('xenographi@gmail.com', 'wzthcfpbtcvnwknl')

	server.sendmail(
		'xenographi@gmail.com',
		'coolman21458905@gmail.com',
		msg
	)
	print('Hey, email has been sent!')

	server.quit()

def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 


link_file = open("linkek.txt", "r")

for adat_harmas in link_file.readlines():
	sor_str = listToString(adat_harmas).rstrip("\n")
	trigger, link, idd, nev, ar = sor_str.split(' ')
	uj_ar = float(ar)
	check_price(trigger, link, idd, nev, uj_ar)
	
link_file.close()
