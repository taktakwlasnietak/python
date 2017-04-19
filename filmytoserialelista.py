from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sys
import time
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('/home/krzys/Downloads/chromedriver')

lines = [line.rstrip('\n') for line in open('odcinkilista')]
x = 0
for l in lines:
	try:
		strona = lines[x]
		driver.get(strona)
		time.sleep(2)

		tytulPL = "[[brak]]"
		tytulENG = "[[brak]]"
		roku = "[[brak]]"
		embedy = ""
		gatunki = "[[brak]]"
		opis = "[[brak]]"
		poster = "[[brak]]"
		tytulODC = "[[brak]]"
		nrODC = "[[brak]]"
		nrSEZONU = "[[brak]]"
		
		try:
			nrse = driver.find_element_by_tag_name("select")
			nrsezo = nrse.find_element_by_xpath("//option[@selected='selected']")
			nrSEZONU = nrsezo.text
		except:
			pass
		
		try:
			tytODC = driver.find_element_by_class_name("episodeLinks")
			try:
				span = tytODC.find_element_by_xpath("//a[@class='active']")
				span1 = span.find_elements_by_tag_name("span")[0]
				nrODC = span1.text
			except:
				tytODC = driver.find_element_by_class_name("episodeLinks")	
				span = tytODC.find_element_by_xpath("//a[@class='active no-hst']")
				span1 = span.find_elements_by_tag_name("span")[0]
				nrODC = span1.text
		except:
			pass
		
		try:
			tytODC = driver.find_element_by_class_name("episodeLinks")
			span = tytODC.find_element_by_xpath("//a[@class='active']")
			span1 = span.find_elements_by_tag_name("span")[1]
			tytulODC = span1.text
		except:
			pass

		try:
			gatunek1 = driver.find_elements_by_tag_name("td")[7]
			gatunek1 = gatunek1.text
			gatunki = gatunek1.replace(" /",",")
		except:
			pass

		try:
			poster1 = driver.find_elements_by_tag_name("img")[1]
			poster = poster1.get_attribute("src")
		except:
			pass

		try:
			opis1 = driver.find_element_by_xpath("//meta[@property='og:description']").get_attribute("content")
			opis = opis1
		except:
			pass

		#pattern na rok
		def rocznik(text):
			if len(text) != 4:
				return False
			for i in range(0,4):
				if not text[i].isdigit():
					return False
			return True

		try:
				
			tytul = driver.find_element_by_class_name("frame-header")
			tytul = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute('content')
			tytPL = tytul
		except:
			pass
			
				#wyciaganie roku z tytulu
		for i in range(len(tytPL)):
			rok = tytPL[i:i+4]
			if rocznik(rok):
				ww = tytPL.split((rok),1)[0]
				if ("/") in tytPL:
					tytulPL = ww.split("/",1)[0]
					tytulENG = ww.split("/",1)[1]
					tytulENG = tytulENG.lstrip()
					roku = rok
				else:
					tytulPL = ww
					tytulENG = "[[brak]]"
					roku = rok
		

		#wyciaganie embedow
		try:
			content = driver.find_element_by_id("content")
			hosting = driver.find_element_by_id("hosting")
			f = driver.find_element_by_class_name("clearfix")
			a = f.find_element_by_id("hosting")
			b = a.find_elements_by_tag_name('div')[1]
			e = b.find_elements_by_xpath("//*[@class='url']")
			for l in e:
				lista = []
				f = l.get_attribute("data-url")
				#print f
				y = re.findall(r'"(.*?)"',f)[0]
				embedy += " !! " + str(y)

				
		except:
			pass
		
		
		if tytulPL == "[[brak]]":
			time.sleep(10)
			x-=1
		else:
			pass
		
		print("%s ## %s ## %s ## %s ## %s ## %s ## %s ## %s ## %s ## %s" % (roku, tytulPL, tytulENG, nrSEZONU, nrODC, tytulODC, opis, gatunki, poster, embedy))
		x+=1
	except:
		print lines[x]
		print "ten wyzej do poprawki"
		x+=1
		pass
