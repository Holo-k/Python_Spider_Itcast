import threading
import json
from lxml import etree
import requests
import time
from queue import Queue


class ThreadCrawl(threading.Thread):
    def __init__(self, threadname, pageQueue, dataQueue):
        super(ThreadCrawl, self).__init__()
        self.threadname = threadname
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
        }

    def run(self):
        print(f'{self.threadname} 启动')
        while not self.pageQueue.empty():
            try:
                # 取出一个数字，先进先出
                # 可选参数block，默认值为True
                #1. 如果对列为空，block为True的话，不会结束，会进入阻塞状态，直到队列有新的数据
                #2. 如果队列为空，block为False的话，就弹出一个Queue.empty()异常，
                page = self.pageQueue.get(False)
                url = f'https://www.qiushibaike.com/8hr/page/{page}/'
                response = requests.get(url, headers=self.headers)
                time.sleep(1)
                self.dataQueue.put(response)
            except Exception as e:
                print('error')
        print(f'结束{self.threadname}')
        print(self.dataQueue.qsize())


class ThreadParse(threading.Thread):
    def __init__(self, threadname, dataQueue, filename, lock):
        super(ThreadParse, self).__init__()
        self.threadname = threadname
        self.dataQueue = dataQueue
        self.filename = filename
        self.lock = lock

    def run(self):
        print(f'{self.threadname} 启动')
        while not self.dataQueue.empty():
            print('-----poi----------')
            try:
                self.parse()
            except Exception as e:
                print('error')
                pass
        print(f'结束{self.threadname}')

    def parse(self):
        # 取出一个数字，先进先出
        # 可选参数block，默认值为True
        #1. 如果对列为空，block为True的话，不会结束，会进入阻塞状态，直到队列有新的数据
        #2. 如果队列为空，block为False的话，就弹出一个Queue.empty()异常，
        data = self.dataQueue.get(False)
        print(data)
        xpathObj = etree.HTML(data)
        content__node_list = xpathObj.xpath(
            '//div[contains(@id, "qiushi_tag")]')
        for content_node in content__node_list:
            username = content_node.xpath('./div/a/@title')[0]
            image = content_node.xpath('.//div[@class="thumb"]//@src')
            content = content_node.xpath('.//div[@class="content"]/span')[
                0].text
            zan = content_node.xpath('.//i')[0].text
            comments = content_node.xpath('.//i')[1].text

            items = {
                "username": username,
                "image": image,
                "content": content,
                "zan": zan,
                "comments": comments
            }

            print(items)
            with self.lock:
                self.filename.write(json.dumps(items), encoding='utf-8')


def main():
    pageQueue = Queue(20)
    for page in range(1, 21):
        pageQueue.put(page)
    dataQueue = Queue()
    filename = open('./xiushi_spider_with_threading/duanzi.json', mode='a+')
    lock = threading.Lock()

    crawlList = ["采集线程1号", "采集线程2号", "采集线程3号"]
    threadcrawl = []
    for threadname in crawlList:
        thread = ThreadCrawl(threadname, pageQueue, dataQueue)
        thread.start()
        threadcrawl.append(thread)

    parseList = ["解析线程1号", "解析线程2号", "解析线程3号"]
    threadparse = []
    for threadname in parseList:
        thread = ThreadParse(threadname, dataQueue, filename, lock)
        thread.start()
        threadparse.append(thread)

    [thread.join() for thread in threadcrawl]

    print('pageQueue为空')

    [thread.join() for thread in threadparse]
    
    with lock:
        filename.close()
    print("谢谢使用！")


if __name__ == '__main__':
    main()