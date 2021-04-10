import requests
from bs4 import BeautifulSoup
import smtplib
import time

rx580_max = 3200

#URL = 'https://www.cel.ro/placi-video/placa-video-xfx-radeon-rx-580-gts-xxx-edition-8gb-gddr5-256bit-pNSM7NT0t-l/'
headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}


def check_price(link, iddd, nev, max_ar):
	
	page = requests.get(link, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	# Ar, es annak atalakitasa
	price = soup.find(id=idd).get_text()
	converted_price = float(price)

	# Kartya nev
	#name = soup.find(id="product-name").get_text();
	name = nev

	# Uzenet kepzes
	subject = 'Price fell down on {}!'.format(nev.upper())
	body = 'New price: {} RON, check the link: {}'.format(converted_price, link)
	msg = 'Subject: {}\n\n{}'.format(subject, body)

	# Kiiras konzolra
	#print(name)
	#print("CEL.ro: ", converted_price)
	#print('\n')

	# Ellenorzes, majd email kuldes a megfelelo uzenettel
	if(converted_price < max_ar):
		send_mail(msg)

def send_mail(msg):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login('xenographi@gmail.com', 'wzthcfpbtcvnwknl')

	#subject = 'Price fell down!'
	#body = 'Check the CEL.ro link: https://www.cel.ro/placi-video/placa-video-xfx-radeon-rx-580-gts-xxx-edition-8gb-gddr5-256bit-pNSM7NT0t-l/'
	
	#msg = 'Subject: {}\n\n{}'.format(subject, body)

	server.sendmail(
		'xenographi@gmail.com',
		'coolman21458905@gmail.com',
		msg
	)
	print('Hey, email has been sent!')

	server.quit()

#while(True):
#check_price()
#	time.sleep(60)

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
	link, idd, nev, ar = sor_str.split(' ')
	uj_ar = float(ar)
	check_price(link, idd, nev, uj_ar)

link_file.close()
