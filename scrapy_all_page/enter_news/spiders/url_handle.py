# coding:utf-8
import urllib2
import hashlib
from lxml import etree

def get_time(url):
    '''获得文章具体时间'''
    html = urllib2.urlopen(url).read()
    selector=etree.HTML(html)
    time= selector.xpath('//div[@class="tip fl"]/span/text()')[0]
    return time

def keywords():
    '''关键字'''
    keywords = ["全球","法国","新规","数字引擎","迪创科技","乐视"]
    return keywords

def except_outside_url():
    '''重点网页监控中已经有的网页'''
    except_outside_url_list = [
        "http://news.hexun.com/original/",
        "http://news.hexun.com/domestic/",
        "http://news.hexun.com/company/",
        "http://news.hexun.com/listedcompany/"]
    return except_outside_url_list

def hash_url_func(url):
    '''对url进行md5加密，去重'''
    m = hashlib.md5()  
    m.update(url)
    hash_url = str(m.hexdigest())
    return hash_url
