__author__ = 'dr644w'
from neomodel import (StructuredNode, StringProperty, IntegerProperty)
from neomodel.exception import UniqueProperty, DeflateError


class Customer(StructuredNode):
    email = StringProperty(unique_index=True, required=True)
    age = IntegerProperty(index=True)


tst = Customer.create({'email':'test@test.com','age':3})

try:
    tst1 = Customer.create({'email':'test@test.com','age':3},{'email':'test1@test.com','age':4})

except Exception as e:
    print e.message



for c in Customer.category().instance.all():
    print c.email
