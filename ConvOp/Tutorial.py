import numpy
import theano
import theano.tensor as T

a = T.vector() # declare variable
b = T.vector() # declare variable
out = a ** 2 + b ** 2 + 2 * a * b # build symbolic expression
f = theano.function([a,b], out)   # compile function