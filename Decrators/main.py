import decrators
import functools
from pet import Pet

# Example 1
def function1():
  print 'Wheee!'

function1 = decrators.simple_decorator(function1)


# Example 2
@decrators.simple_decorator
def function2():
  print("Yeah!")


# Example 3
@decrators.timing_function
def CreateList():
  num_list = []
  for num in range(0, 101):
    num_list.append(num)
  print 'Sum of all the numbers: ' + str(sum(num_list))

# equivalent to:
# CreateList = decrators.timing_function(CreateList)


# Example 4
@decrators.sleep_for(0.5)
def print_number(num):
  print num

# equivalent to:
# print_number = decrators.sleep_for(0.5)(print_number)


@decrators.login_required
def show_data():
  print 'secret picture'


def f(a, b, c, d=0):
  print a, b, c, d

def wrapper_1(num, *args, **kwargs):
  print args
  print kwargs
  return f(num, *args, **kwargs)


pet = Pet(name='snoopy', age=3)

@decrators.mock_patch_object(pet, 'wakeup')
@decrators.mock_patch_object(pet, 'sleep')
def testPet(mock_sleep, mock_wakeup):
  mock_sleep.return_value = 'hehe'
  mock_wakeup.return_value = 'oh'
  print pet.sleep()
  print pet.wakeup()


@decrators.accepts(float, (int, float, int))
def func(arg1, arg2, arg3):
  return arg1 * arg2


if __name__ == '__main__':
  # function1()
  # function2()
  
  # print CreateList()

  # for num in range(1, 4):
  #   print_number(num)

  # show_data()
  # show_data()

  pet.sleep()
  testPet()
  pet.sleep()

  # g = functools.partial(f, 3)
  # g(4, 5, d=6)

  # print func(3, 2.0, 1)
  # print func('3', 2, 1)