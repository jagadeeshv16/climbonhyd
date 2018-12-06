from selenium import webdriver
from pyvirtualdisplay import Display
import time
import requests

display = Display(visible=0, size=(1366, 768))
display.start()
driver = webdriver.Firefox()
driver.get("https://www.instagram.com/climbon_hyderabad/")
time.sleep(2)
url = []
lenOfPage=driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
shortcode = driver.find_elements_by_class_name("FyNDV")
time.sleep(2)
for i in shortcode:
	ele=i.find_elements_by_css_selector('a')
	for j in ele:
		lis=j.get_attribute('href')
		url.append(lis)
		# print (j.get_attribute('href'))
match=False
while(match==False):
	last=lenOfPage
	lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	time.sleep(2)
	if last!=lenOfPage:
		shortcode = driver.find_elements_by_class_name("FyNDV")
		time.sleep(2)
		for i in shortcode:
			ele=i.find_elements_by_css_selector('a')
			for j in ele:
				lis=j.get_attribute('href')
				url.append(lis)
				# print (j.get_attribute('href'))
	else:
		match=True
		
# print(url,len(url),len(set(url)))
total=list(set(url))
main =[]
# print(total,len(set(url)))
for l in total:
	team="https://api.instagram.com/oembed/?url="+l
	main.append(team)
print(len(main))
display.stop()

# def get(request):
for i in main:
	url=requests.get(i)
	if url.status_code == 200:
		events = url.json()
		print("events",events)

