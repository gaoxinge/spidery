# spidery

spidery is a microframework for web crawler, and it has many features such as
- spidery has a top-to-bottom design, which is inspired by [flask](https://github.com/pallets/flask)
- it is also light because spidery only provides a web crawler engine to dispatch works, instead of other network libraries, parsers or database connections 
- it can deal with structural data because it provides a metaclass to create named dictionary with a fixed field
- spidery is based on multithread
- it supports `pip install spidery`

## example

- [stackoverflow](https://github.com/For-Human/spidery/blob/master/example/stackoverflow.py)
- [douban](https://github.com/For-Human/spidery/blob/master/example/douban.py)
- [github](https://github.com/For-Human/spidery/blob/master/example/github.py)

## API

### Spider

It is a consumer class, which dispatches worker to handle the url.

```python
from spidery import Spider
spider = Spider( # initialize an instance spider
    urls   = ['https://github.com/gaoxinge?tab=following'],
    filter = set(['https://github.com/gaoxinge?tab=following']),
)
```

- decorator and run

```python
from spidery import Spider

spider = Spider([_ for _ in range(1000)])
sum = 0

@spider.http
def http(url):
    return url*url

@spider.parse
def parse(response):
    global sum
    spider.lock.acquire()
    sum += response
    spider.lock.release()
    return []
    
@spider.save
def save(item):
    pass
    
spider.run(5) # open 5 workers
print sum
```

- log

```python
from spidery import Spider
spider = Spider([])
spider.log('step', 'status', 'message')
```

- add

add is used to filter and save new url, which is parsed from parse step.

- lock

lock is 'global' in Spider, and can control the resources.

### Item

It is a tool, which can create a named dictionary, to save structural data. It is inspired by the namedtuple in collections module, and is a metaclass to create dictionary with a name and a fixed field.

```python
from spidery import Item
Question = Item('Question', ['votes', 'answers', 'views', 'title', 'link'])
question = Question(
    votes   = '6210',
    answers = '33',
    views   = '1246228',
    title   = 'What does the \'yield\' keyword do in Python?',
    link    = 'http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python',
)
```

## TODO

- support python3
- http preprocessor, like login.
- use bloomfilter