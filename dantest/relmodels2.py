from neomodel import (StructuredNode, StructuredRel, Relationship, RelationshipTo,
        StringProperty, DateTimeProperty, DeflateError)
from datetime import datetime
import pytz


class FriendRel(StructuredRel):
    since = DateTimeProperty(default=lambda: datetime.utcnow())


class HatesRel(FriendRel):
    reason = StringProperty()


class Badger(StructuredNode):
    name = StringProperty(unique_index=True)
    friend = Relationship('Badger', 'FRIEND', model=FriendRel)
    hates = RelationshipTo('Stoat', 'HATES', model=HatesRel)


class Stoat(StructuredNode):
    name = StringProperty(unique_index=True)
    hates = RelationshipTo('Badger', 'HATES', model=HatesRel)



paul = Badger(name="Paul the badger").save()
ian = Stoat(name="Ian the stoat").save()

rel = ian.hates.connect(paul, {'reason': "thinks paul should bath more often"})
assert isinstance(rel.since, datetime)
assert isinstance(rel, FriendRel)
assert rel.reason.startswith("thinks")
rel.reason = 'he smells'
rel.save()

ian = rel.start_node()
assert isinstance(ian, Stoat)
paul = rel.end_node()
assert isinstance(paul, Badger)

assert ian.name.startswith("Ian")
assert paul.name.startswith("Paul")

rel = ian.hates.relationship(paul)
assert isinstance(rel, HatesRel)
assert isinstance(rel.since, datetime)
rel.save()

# test deflate checking
rel.since = "2:30pm"
try:
    rel.save()
except DeflateError:
    assert True
else:
    assert False

# check deflate check via connect
try:
    paul.hates.connect(ian, {'reason': "thinks paul should bath more often", 'since': '2:30pm'})
except DeflateError:
    assert True
else:
    assert False