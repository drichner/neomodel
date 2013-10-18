from neomodel import StructuredNode, StringProperty, CypherException


class User2(StructuredNode):
    email = StringProperty()


jim = User2(email='jim1@test.com').save()
email = jim.cypher("START a=node({me}) RETURN a.email").data[0][0]
assert email == 'jim1@test.com'