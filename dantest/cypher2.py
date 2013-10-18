from neomodel import StructuredNode, StringProperty, CypherException
from py2neo.exceptions import ClientError

class User2(StructuredNode):
    email = StringProperty()

jim = User2(email='jim1@test.com').save()
try:
    jim.cypher("START a=node({me}) RETURN xx")
except CypherException as e:
    assert hasattr(e, 'message')
    print e
else:
    assert False