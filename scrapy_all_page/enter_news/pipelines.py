# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class EnterNewsPipeline(object):
    def process_item(self, item, spider):
    	filrname = item["url_path"]
    	f = open("./file/"+filrname+".txt","a")
    	f.write(item["url_name"]+","+item["url"]+"\n")
    	f.close()
        return item

