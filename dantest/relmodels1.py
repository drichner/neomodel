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



paul = Badger(name="Paul").save()
tom = Badger(name="Tom").save()

# creating rels
new_rel = tom.friend.disconnect(paul)
new_rel = tom.friend.connect(paul)
assert isinstance(new_rel, FriendRel)
assert isinstance(new_rel.since, datetime)

# updating properties
new_rel.since = datetime.now(pytz.utc)
assert isinstance(new_rel.save(), FriendRel)

# start and end nodes are the opposite of what you'd expect when using either..
# I've tried everything possible to correct this to no avail
paul = new_rel.start_node()
tom = new_rel.end_node()
assert paul.name == 'Paul'
assert tom.name == 'Tom'
