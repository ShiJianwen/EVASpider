# -*- coding: utf-8 -*-
import time, Queue, threading, urllib2, urllib, re, uuid
from multiprocessing.managers import BaseManager
from bs4 import BeautifulSoup

class QueueManager(BaseManager): 
	pass

#用名字注册两个队列
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

#给本机一个唯一标识
host = uuid.uuid4()

#连接服务器
m = QueueManager(address=('127.0.0.1', 50000), authkey='spider_man')
m.connect()
print '服务器连接成功...'

#获取任务队列和结果队列
task = m.get_task_queue()
result = m.get_result_queue()

#执行任务的函数
def do_work(task, result):
	while True:
		if task.empty() == False:
			url = task.get()
			print '开始执行任务...'
			html = urllib2.urlopen(url).read()
			soup = BeautifulSoup(html)
			title = soup.find('title').string
			f = open('./results/'+title+'.html', 'w+')
			f.write(soup.encode('utf-8'))
			f.close()
			r_str = 'host:{0}, title:{1}'.format(host, title.encode('utf-8'))
			print r_str
			result.put(r_str)
		else:
			time.sleep(3)

#开启一条线程运行执行任务的函数
threading.Thread(target=do_work, args=(task, result)).start()