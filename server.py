# -*- coding: utf-8-*-
#author:ShiJianwen
import urllib, urllib2, re, Queue, threading, time
from multiprocessing.managers import BaseManager

#任务队列
task_queue = Queue.Queue()
#结果队列
result_queue = Queue.Queue()

class QueueManager(BaseManager): 
	pass

#注册任务队列
QueueManager.register('get_task_queue', callable=lambda:task_queue)
#注册结果队列
QueueManager.register('get_result_queue', callable=lambda:result_queue)
#开启主进程服务器
m = QueueManager(address=('127.0.0.1', 50000), authkey='spider_man')
m.start()

#获取任务队列
online_task_queue = m.get_task_queue()
#获取结果队列
online_result_queue = m.get_result_queue()

#定义全局变量
host_url = 'http://segmentfault.com/'
current_page = 1

#抓取问题链接放入任务队列中
def get_url(page):
	res = urllib2.urlopen(host_url+'questions?page='+str(page))
	html = res.read()
	#构建问题链接的正则表达式
	question_link_pattern = re.compile("<a href=\"/q/\d+\">")
	url_pattern = re.compile("q/\d+")
	question_link_list = question_link_pattern.findall(html)
	for i in question_link_list:
		url = url_pattern.search(i).group()
		online_task_queue.put(host_url+url)
	print '任务分配成功，当前任务数：', online_task_queue.qsize()

#分配任务函数
def divide_task(task):
	global current_page
	while True:
		if task.empty() == False:
			time.sleep(1)
		else:
			print '当前任务队列为空，自动获取新的任务...'
			get_url(current_page)
			current_page = current_page + 1

#获取结果函数
def get_result(result):
	while True:
		if result.empty() == False:
			r = result.get()
			print '任务完成，结果：{0}，剩余任务：{1} '.format(r, online_task_queue.qsize())
		else:
			time.sleep(1)

#启用两条线程分别运行任务分配和结果接收的函数
print '启动任务分配线程...'
threading.Thread(target=divide_task, args=(online_task_queue,)).start()

print '启动接收结果线程...'
threading.Thread(target=get_result, args=(online_result_queue,)).start()



