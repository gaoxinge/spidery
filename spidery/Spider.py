# -*- coding: utf-8 -*-
import threading

class Worker(threading.Thread):
    """Worker is a thread class, which is used
    to handle the url by creating a new thread.
    
    :param queue: the tunnel to get the url
    :param f: the function to handle the url
    """
    
    def __init__(self, queue, f):
        threading.Thread.__init__(self)
        self.queue = queue
        self.f = f
    
    def run(self):
        while True:
            url = self.queue.get()
            if url == 'exit':
                break
            self.f(url)

class Spider(object):
    """Spider is a consumer class, which dispatches
    worker to handle the url.
    
    :param urls: the initializing urls
    :parma filter: the initializing filter rule
    """
    
    def __init__(self, urls, filter=None):
        self.urls = urls
        self.filter = filter
        self.lock = threading.Lock()
        self.config = None
        self.steps = {
            'http':  None,
            'parse': None,
            'save': None,
        }
    
    def log(self, step, status, message):
        import datetime
        self.lock.acquire()
        print '[{a}][{b}][{c}] {d}'.format(
            a=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            b=step,
            c=status,
            d=message,
        )
        self.lock.release()
        
    def http(self, f):
        self.steps['http'] = f
        return f
        
    def parse(self, f):
        self.steps['parse'] = f
        return f

    def save(self, f):
        self.steps['save'] = f
        return f
    
    def add(self, url):
        self.lock.acquire()
        if url not in self.filter:
            self.urls.append(url)
            self.filter.add(url)
        self.lock.release()
    
    def http_parse_save(self, url):
        response = self.steps['http'](url)
        items = self.steps['parse'](response)
        for item in items:
            self.steps['save'](item)
            
    def run(self, num):
        import Queue
        queue = Queue.Queue()
        workers = []
        for _ in range(num):
            worker = Worker(queue, self.http_parse_save)
            workers.append(worker)
            worker.start()
        flag = True
        
        while True:
            if self.urls and len(self.filter) < 100:
                url = self.urls.pop(0)
                queue.put(url)
                for _ in workers:
                    if not _.is_alive():
                        workers.remove(_)
                        worker = Worker(queue, self.http_parse_save)
                        workers.append(worker)
                        worker.start()
            elif flag:
                for _ in range(num):
                    queue.put('exit')
                flag = False
            else:
                count = 0
                for _ in workers:
                    if not _.is_alive():
                        count += 1
                    else:
                        continue
                if count == num:
                    break
                    
        if self.config is not None:
            self.config.close()