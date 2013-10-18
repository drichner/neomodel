from neomodel import StructuredNode, StringProperty, IntegerProperty, UniqueProperty
from lucenequerybuilder import Q


class Human(StructuredNode):
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True)



Human(name="j1m", age=13).save()
try:
    Human(name="j1m", age=14).save()
except Exception as e:
    assert True
    assert str(e).find('j1m')
    assert str(e).find('name')
    assert str(e).find('FooBarr')
    print str(e)
else:
    assert False