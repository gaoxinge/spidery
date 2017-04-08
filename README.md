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

### spidery.Spider

### spidery.Item

Item is a tool, which can create a named dictionary, to save structural data. It is inspired by the namedtuple in collections module, and is a metaclass to create dictionary with a name and a fixed field.

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