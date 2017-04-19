#scraping movie links with info from filiser.tv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sys
import time
from selenium.common.exceptions import NoSuchElementException

lines = [line.rstrip('\n') for line in open('filiserlista2')]
x=0
driver = webdriver.Chrome('/home/krzys/Downloads/chromedriver')

for l in lines:
	try:
		driver.get(lines[x])
		titleENG #tytulENG = "[[brak]]"
		genres #gatunek = "[[brak]]"
		description #opis = "[[brak]]"
		year #rocznik = "[[brak]]"
		try:
			desc = driver.find_element_by_id('desc')
			description = desc.text
		except NoSuchElementException:
			pass

		pl = driver.find_element_by_class_name('title')
		titlePL = pl.text

		try:
			genre = driver.find_element_by_id("genres")
			genres = genre.text
		except NoSuchElementException:
			pass

		try:
			h1tag = driver.find_element_by_tag_name('h1')
			eng = driver.find_element_by_tag_name('h3')
			titleENG = eng.text
		except NoSuchElementException:
			pass

		try:
			yearp = driver.find_element_by_id("year")
			yearp = year.text
			rocznik = yearp.replace("Premiera: ", "",1)
		except NoSuchElementException:
			pass

		try:
			block = driver.find_element_by_class_name("title_block")
			x+=1
		except NoSuchElementException:
			pass

		try:
			nolinks = driver.find_element_by_class_name("no_data")
			x+=1
		except NoSuchElementException:
			pass

		iframe = driver.find_elements_by_tag_name("iframe")[0]
		driver.switch_to_frame(iframe)
		openload = driver.find_element_by_xpath("//iframe").get_attribute('src')

		if openload.startswith('chuj'):
			driver.refresh()
			iframe = driver.find_elements_by_tag_name("iframe")[0]
			driver.switch_to_frame(iframe)
			openload = driver.find_element_by_xpath("//iframe").get_attribute('src')
		elif openload.startswith('https://www.google.com'):
			time.sleep(10)
		else:
			print("%s ## %s ## %s ## %s ## %s ## %s ## tuPosTer") % (year, titlePL, titleENG, description, genres, openload)
			x=x+1
	except:
		time.sleep(10)
		pass
