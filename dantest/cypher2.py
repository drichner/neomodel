from neomodel import StructuredNode, StringProperty, CypherException


class User2(StructuredNode):
    email = StringProperty()

jim = User2(email='jim1@test.com').save()
try:
    jim.cypher("START a=node({me}) RETURN xx")
except Exception as e:
    assert hasattr(e, 'message')
    assert hasattr(e, 'query')
    assert hasattr(e, 'query_parameters')
    assert hasattr(e, 'java_trace')
    assert hasattr(e, 'java_exception')
else:
    assert False