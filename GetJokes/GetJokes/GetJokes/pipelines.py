# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import cymysql

class GetjokesPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqldbPipeline(object):
	conn = None
	def __init__(self):
		pass
	def open_spider(self, spider):
		self.conn = cymysql.connect(host='127.0.0.1', user='root', passwd='',db='jokes')
		#self.conn = cymysql.connect(host='127.0.0.1', user='ethionhh_idcard', passwd='ic350909',db='ethionhh_idcard')
		self.cur = self.conn.cursor()
		print('db connection opened')
	def close_spider(self, spider):
		self.conn.close()
		print('db connection closed')
		
	def process_item(self, item, spider):
		columns = ['title', 'content', 'joke_class']
		insert_statment = 'INSERT INTO tjokelist({0}) values({1})'.format(','.join(columns), ','.join(['%s']*(len(columns)))) 
		try:
			self.cur.execute(insert_statment,(item[columns[0]],item[columns[1]],item[columns[2]]))
			self.conn.commit()
		except Exception as e:
			print(e)
