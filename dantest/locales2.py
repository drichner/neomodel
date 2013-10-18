from neomodel import StructuredNode, StringProperty
from neomodel.contrib import Localised, Locale


class Student(Localised, StructuredNode):
    name = StringProperty(unique_index=True)



for l in ['fr', 'ar', 'pl', 'es']:
    Locale(code=l).save()


fred = Student(name="Fred").save()
jim = Student(name="Jim").save()
katie = Student(name="Katie").save()

fred.add_locale(Locale.get('fr'))
jim.add_locale(Locale.get('fr'))
katie.add_locale(Locale.get('ar'))

assert Student.locale_index('fr').get(name='Fred')
assert len(Student.locale_index('fr').search('name:*')) == 2

try:
    Student.locale_index('fr').get(name='Katie')
except Student.DoesNotExist:
    assert True
else:
    assert False
