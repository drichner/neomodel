__author__ = 'dr644w'
from neomodel import (StructuredNode, StringProperty, IntegerProperty)
from neomodel.exception import UniqueProperty, DeflateError

class Customer(StructuredNode):
    email = StringProperty(unique_index=True, required=True)
    age = IntegerProperty(index=True)
try:
    tst = Customer.index.get(email='test@test.com')
    tst.delete()
except:
    pass
tst1 = Customer(email='test@test.com',age=3)
tst1.save()

for c in Customer.category().instance.all():
    print c
