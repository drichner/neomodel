__author__ = 'dr644w'

from neomodel import (StructuredNode, StringProperty, IntegerProperty,
        RelationshipTo, AttemptedCardinalityViolation, CardinalityViolation,
         OneOrMore, ZeroOrMore, ZeroOrOne, One)


class HairDryer(StructuredNode):
    version = IntegerProperty()


class ScrewDriver(StructuredNode):
    version = IntegerProperty()


class Car(StructuredNode):
    version = IntegerProperty()


class Monkey(StructuredNode):
    name = StringProperty()
    dryers = RelationshipTo('HairDryer', 'OWNS_DRYER', cardinality=ZeroOrMore)
    driver = RelationshipTo('ScrewDriver', 'HAS_SCREWDRIVER', cardinality=ZeroOrOne)
    car = RelationshipTo('Car', 'HAS_CAR', cardinality=OneOrMore)
    toothbrush = RelationshipTo('ToothBrush', 'HAS_TOOTHBRUSH', cardinality=One)


class ToothBrush(StructuredNode):
    name = StringProperty()

m = Monkey(name='bob').save()
assert m.driver.all() == []
assert m.driver.single() == None
h = ScrewDriver(version=1).save()

m.driver.connect(h)
assert len(m.driver.all()) == 1
assert m.driver.single().version == 1

j = ScrewDriver(version=2).save()
try:
    m.driver.connect(j)
except AttemptedCardinalityViolation:
    assert True
else:
    assert False

m.driver.reconnect(h, j)
assert m.driver.single().version == 2