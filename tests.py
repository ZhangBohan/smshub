import unittest
import leancloud

from datetime import datetime, date
from leancloud import Object


class LearnCloudTest(unittest.TestCase):
    def setUp(self):
        leancloud.init('acp50a9n4qd9ycr4fc1a4quxuxlj9r28o9rda334pqkv2hzw', '12ebc1ue2bwoj6ozp79ihf8fx1yclpimrvan24mgphhylnpb')

    def test_date_time_type(self):
        obj = Object.extend('myObject')()
        obj.set('myNumber', 2.718)
        obj.set('myString', 'foobar')
        obj.set('myDate', datetime.now())
        obj.set('myArray', [1, 2, 3, 4])
        obj.set('myDict', {'string': 'some string', 'number': 1})
        obj.set('myNone', None)
        obj.save()

    def test_date_type(self):
        obj = Object.extend('myObject')()
        obj.set('myNumber', 2.718)
        obj.set('myString', 'foobar')
        obj.set('myDate', date.today())
        obj.set('myArray', [1, 2, 3, 4])
        obj.set('myDict', {'string': 'some string', 'number': 1})
        obj.set('myNone', None)
        obj.save()