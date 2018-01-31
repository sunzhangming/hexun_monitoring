# -*- coding: utf-8 -*-
# from __future__ import absolute_import
from enter_news.items import EnterNewsItem
import os
import re
import time
import redis
import scrapy
import url_handle


class HexunSpider(scrapy.Spider):
    name = 'hexun'
    allowed_domains = ['hexun.com']
    start_urls = ['http://www.hexun.com/']

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)        
        self.t = time.strftime('%Y-%m-%d',time.localtime(time.time()))  # 获取今日日期：0000-00-00
        self.f = open("aim_xinwen.txt","a") # 目标新闻保存
        self.errortxt = open("error_url.txt","a") # 错误信息保存 

    def parse(self, response):
        global keyword, url, url_path, url_name, item
        repetition_url = url_handle.except_outside_url() # 获取"重点网页爬取"中的网页，防止重复爬取
        item = EnterNewsItem()
        all_url_label = response.xpath("//a") # 获取网页上所有<a>
        for url_label in all_url_label:
            try:
                url = url_label.xpath("./@href").extract_first()
                url_name = url_label.xpath("./text()").extract_first()
                if (url is None or url_name is None or (url.find("javascript:") != -1) 
                    or url == "#" or url in repetition_url): # 无效网址们
                    continue
                url = url.encode("utf-8")
                url_name  = url_name.encode("utf-8")
                url_p_split = url.split("/") # 将得到的url进行切割，方便判断
                url_p2_split = url_p_split.pop().split(".") # 操作192331729.html部分
                url_path = url_p_split.pop() # 将2018-01-29这部分类型作为存储区分
                y = re.match(r'^http://.*?/[0-9]{4}-[0-9]{2}-[0-9]{2}/[0-9]{9}\.html$',url)
                # 判断http://gold.hexun.com/2018-01-29/192331729.html类型的url
                if y:
                    if url_path == self.t: # 爬取今日数据
                        if(not os.path.exists("./file/"+url_path+".txt")):
                            os.mknod("./file/"+url_path+".txt") # 如果目录不存在，则创建目录
                        url_name = url_name.strip()
                        hash_url = url_handle.hash_url_func(url) # 对url进行md5加密
                        result = self.r.sismember("hexun",hash_url) 
                        if not result: # 判断html是否保存过
                            self.r.sadd("hexun",hash_url) 
                            keywords = url_handle.keywords() # 获得需要判断的企业名称
                            for keyword in keywords:
                                keyword.decode("utf-8")
                                j = self.judge(keyword,url_name,url,url_path)
                                if j: # 新闻判断一次即可
                                    break
                            yield item
                else:
                    yield scrapy.Request(url, callback = self.parse)
            except Exception as e:
                self.errortxt.write(self.t +url_name+url+"\n")

    def judge(self,keyword,url_name,url,url_path):
        '''判断最新更新的新闻是不是有目标企业'''
        if url_name.find("%s"%keyword) !=-1: # 标题中是否含有目标企业
            time = url_handle.get_time(url)
            self.f.write(time+url_name+url+"\n")
        else:
            item["url_path"] = url_path
            item["url_name"] = url_name
            item["url"] = url
            return True



      
    
   
 

        
