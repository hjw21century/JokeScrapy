# -*- coding: utf-8 -*-
import scrapy
from GetJokes.items import GetjokesItem
import time 

count = 1

class GetlatestjokeSpider(scrapy.Spider):
    name = "getlatestjoke"
    allowed_domains = ["http://www.jokeji.cn"]
    dont_filter=True
    meta={'dont_redirect': True}
    start_urls = ['http://www.jokeji.cn/list_1.htm']
    #map(lambda elem: 'http://http://www.jokeji.cn/list_' + str(elem) + '.htm',range(1,9+1))
    base_url = 'http://www.jokeji.cn'

    

    def parse(self, response):
    	sel=scrapy.Selector(response)
    	jokes=sel.css('.joke_left li')
    	for joke in jokes:
    		joke_url = self.base_url + joke.css('b a::attr(href)').extract()[0]
    		if(joke_url is not None):
    			yield scrapy.Request(joke_url, meta = {
                      'dont_redirect': True,
                      'handle_httpstatus_list': [302]
                  },
                  callback=self.parsejoke,
                  dont_filter=True)
    	time.sleep(5)
    	global count
    	if count < 564+1:
    		print("----------" + str(count) + "---------")
    		count = count + 1
    		next_url = 'http://www.jokeji.cn/list_' + str(count) + '.htm'
    		print("----------" + str(count) + "---------")
    		print("next url : " + next_url)
    		yield scrapy.Request(next_url, meta = {
                      'dont_redirect': True,
                      'handle_httpstatus_list': [302]
                  },
                  callback=self.parse, dont_filter=True)
    	


    def parsejoke(self, response):
    	sel=scrapy.Selector(response)
    	joke_class = ' '.join(sel.css('a[title=查看此类型的所有笑话]::text').extract())
    	title = sel.css('h1::text').extract()[1].split(' ')[2]
    	jokes = sel.css('span p')
    	for joke in jokes:
    		try:    		
    			joke_item = GetjokesItem()
    			joke_item['content'] = '\n'.join(joke.css('::text').extract())
    			joke_item['title'] = title
    			joke_item['joke_class'] = joke_class
    			#time.sleep(1.0/len(jokes))
    			yield joke_item
    		except Exception as e:
    			print(e)






