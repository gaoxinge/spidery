# -*- coding: utf-8 -*-

def Item(name, field):
    """Item is a tool, which can create a named dictionary, to save 
    structural data. It is inspired by the namedtuple in collections 
    module, and is a metaclass to create dictionary with a name and 
    a fixed field.
    
    :param name: the name of dictionary
    :param field: the field of dictionary
    :return: a named dictionary
    
    Usage::
        
        from spidery import Item
        Question = Item('Question', ['votes', 'answers', 'views', 'title', 'link'])
        question = Question()
        question['votes']   = '6210'
        question['answers'] = '33'
        question['views']   = '1246228'
        question['title']   = 'What does the \'yield\' keyword do in Python?'
        question['link']    = 'http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python'
    """

    # check whether field is a list
    # check whether value in field is unique
    if not isinstance(field, list):
        raise TypeError('%s is not a list' % str(field))

    for _ in field:
        if field.count(_) != 1:
            raise ValueError('%s is not unique in %s' % (str(_), str(field)))

    # Attributes::
    #
    #   _field, __slots__, __init__
    #   __getitem__, __setitem__, __delitem__
    #   keys, values, items
    #   __iter__, __len__, __str__, __repr__
    attrs = {}

    def __init__(self, **args):
        self._d = {}
        for _ in args:
            if _ not in self._field:
                raise ValueError('%s is not in %s' % (str(_), str(self._field)))
            self._d[_] = args[_]

    def __getitem__(self, x):
        return self._d[x]

    def __setitem__(self, x, y):
        if x not in self._field:
            raise ValueError('%s is not in %s' % (str(x), str(self._field)))
        else:
            self._d[x] = y

    def __delitem__(self, x):
        del self._d[x]

    def keys(self):
        return self._d.keys()

    def values(self):
        return self._d.values()

    def items(self):
        return self._d.items()

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __str__(self):
        return str(self._d)

    def __repr__(self):
        return repr(self._d)
    
    attrs['_field']    = field
    attrs['__slots__'] = ('_d', )
    attrs['__init__'] = __init__    
    attrs['__getitem__'] = __getitem__
    attrs['__setitem__'] = __setitem__
    attrs['__delitem__'] = __delitem__
    attrs['keys']   = keys
    attrs['values'] = values
    attrs['items']  = items
    attrs['__iter__'] = __iter__
    attrs['__len__']  = __len__
    attrs['__str__']  = __str__
    attrs['__repr__'] = __repr__

    return type(name, (object, ), attrs)
