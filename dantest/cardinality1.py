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

m = Monkey(name='tim').save()
t=  m.dryers.all()
s= m.dryers.single()
h = HairDryer(version=1).save()

m.dryers.connect(h)
assert len(m.dryers.all()) == 1
assert m.dryers.single().version == 1

m.dryers.disconnect(h)
assert m.dryers.all() == []
assert m.dryers.single() == None
