import os
import time 

while True:
	os.system("scrapy crawl hexun")
	time.sleep(3600) # 1*60*60 = 3066 run by one hour