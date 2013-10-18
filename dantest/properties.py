from neomodel.properties import (IntegerProperty, DateTimeProperty,
    DateProperty, StringProperty, JSONProperty)
from neomodel.exception import InflateError, DeflateError
from neomodel import StructuredNode
from pytz import timezone
from datetime import datetime, date

class FooBar(object):
    pass


prop = DateTimeProperty()

prop.name = 'foo'
prop.owner = FooBar
t = datetime.utcnow()
print t.utctimetuple()
gr = timezone('Europe/Athens')
gb = timezone('Europe/London')
dt1 = gr.localize(t)
dt2 = gb.localize(t)
print prop.deflate(dt1)
time1 = prop.inflate(prop.deflate(dt1))
tt = time1.utctimetuple()
tt1 = dt1.utctimetuple()
print tt
print dt1
print tt1
assert time1.utctimetuple() == dt1.utctimetuple()
time2 = prop.inflate(prop.deflate(dt2))

assert time1.utctimetuple() < time2.utctimetuple()
assert time1.tzname() == 'UTC'