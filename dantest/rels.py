from neomodel import (StructuredNode, RelationshipTo, RelationshipFrom,
        Relationship, StringProperty, IntegerProperty, One)


class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True)
    is_from = RelationshipTo('Country', 'IS_FROM')
    knows = Relationship('Person', 'KNOWS')

    @property
    def special_name(self):
        return self.name

    def special_power(self):
        return "I have no powers"


class Country(StructuredNode):
    code = StringProperty(unique_index=True)
    inhabitant = RelationshipFrom(Person, 'IS_FROM')
    president = RelationshipTo(Person, 'PRESIDENT', cardinality=One)


class SuperHero(Person):
    power = StringProperty(index=True)

    def special_power(self):
        return "I have powers"


rey = Person(name='Rey', age=3).save()
sakis = Person(name='Sakis', age=3).save()

rey.knows.connect(sakis)
assert rey.knows.is_connected(sakis)
assert sakis.knows.is_connected(rey)
sakis.knows.connect(rey)

result = sakis.cypher("""START us=node({me}), them=node({them})
        MATCH (us)-[r:KNOWS]-(them) RETURN COUNT(r)""",
        {'them': rey.__node__._id})
assert int(result.data[0][0]) == 1

u = Person(name='Mar', age=20).save()
assert u

c = Country(code='AT').save()
assert c

c2 = Country(code='LA').save()
assert c2

c.inhabitant.connect(u, properties={'city': 'Thessaloniki'})
assert c.inhabitant.is_connected(u)

# Check if properties were inserted
result = u.cypher('START root=node:Person(name={name})' +
    ' MATCH root-[r:IS_FROM]->() RETURN r.city', {'name': u.name})[0]
assert result and result[0] == 'Thessaloniki'

u.is_from.reconnect(c, c2)
assert u.is_from.is_connected(c2)

# Check if properties are transferred correctly
result = u.cypher('START root=node:Person(name={name})' +
    ' MATCH root-[r:IS_FROM]->() RETURN r.city', {'name': u.name})[0]
assert result and result[0] == 'Thessaloniki'
