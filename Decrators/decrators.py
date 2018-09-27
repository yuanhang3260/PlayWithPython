import time
import os
from mock import Mock
import functools
from functools import wraps

def simple_decorator(func):

  def wrapper():
    print 'Something is happening before func() is called.'
    func()
    print 'Something is happening after func() is called.'

  return wrapper


def timing_function(func):
  """Outputs the time a function takes to execute."""

  def wrapper():
    t1 = time.time()
    func()
    t2 = time.time()
    return 'Time it took to run the function: ' + str(t2 - t1)

  return wrapper


def sleep_for(seconds):
  """Limits how fast the function is called."""

  def wrapper(func):
    def inner_wrapper(*args, **kwargs):
      time.sleep(seconds)
      return func(*args, **kwargs)
    return inner_wrapper

  return wrapper


# A fake user management system.
class UserSystem(object):
  def __init__(self):
    self._user = ''

  def login(self):
    name = raw_input('Enter your name : ')
    print 'log in as %s' % name
    self._user = name

  def current_user(self):
    return self._user

  def login_and_rediret(self, f, *args, **kwargs):
    self.login()
    f(*args, **kwargs)

login_system = UserSystem()


def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not login_system.current_user():
      login_system.login_and_rediret(f, *args, **kwargs)
    else:
      f(*args, **kwargs)

  return decorated_function


# This is a method mock decrator.
def mock_patch_object(mock_object, mock_method):
  """A simple mock patch."""

  def wrapper(func):

    @wraps(func)
    def inner_wrapper(*args, **kwargs):
      # partial_f = functools.partial(func, m)
      # return partial_f(*args, **kwargs)
      orig_attr = getattr(mock_object, mock_method)
      m = Mock()
      setattr(mock_object, mock_method, m)

      rv = func(m, *args, **kwargs)

      # restore the original attr (method).
      setattr(mock_object, mock_method, orig_attr)
      return rv

    return inner_wrapper

  return wrapper


# Decrator to check function arg and return type.
def accepts(*types):
  assert len(types) == 2
  return_type = types[0]
  args_types = types[1]

  def check_accepts(f):
    assert len(args_types) == f.func_code.co_argcount

    @wraps(f)
    def new_f(*args, **kwds):
      for (a, t) in zip(args, args_types):
        assert isinstance(a, t), "arg %r does not match %s" % (a,t)
      rv = f(*args, **kwds)
      assert isinstance(rv, return_type), "return value %r does not match %s" % (rv, return_type)
      return rv

    return new_f

  return check_accepts
