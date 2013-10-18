from neomodel.traversal import TraversalSet
from neomodel import (StructuredNode, RelationshipTo, StringProperty)


class Shopper(StructuredNode):
    name = StringProperty(unique_index=True)
    friend = RelationshipTo('Shopper', 'FRIEND')
    thebasket = RelationshipTo('Basket', 'TheBASKET')


class ShoppingItem(StructuredNode):
    name = StringProperty()


class Basket(StructuredNode):
    item = RelationshipTo([ShoppingItem], 'ITEM')


def setup_shopper(name, friend):
    jim = Shopper(name=name).save()
    bob = Shopper(name=friend).save()
    b = Basket().save()
    si1 = ShoppingItem(name='Tooth brush').save()
    si2 = ShoppingItem(name='Screwdriver').save()
    b.item.connect(si1)
    b.item.connect(si2)
    jim.friend.connect(bob)
    bob.thebasket.connect(b)
    return jim

bill = setup_shopper('bill', 'ted')
result = bill.traverse('friend').traverse('thebasket').traverse('item').run()
for i in result:
    assert i.__class__ is ShoppingItem
    print i.name


assert 'Screwdriver' in [i.name for i in result]