import os
import mock

class Pet(object):
  def __init__(self, name='', age=0):
    self._name = name
    self._age = age

  def __str__(self):
    return '(%s, %d)' % (self._name, self._age)

  def sleep(self):
    print 'sleeping ...'

  def wakeup(self):
    print 'wake up'

