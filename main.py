import math
import numpy as np  # could probably do without, but why reinvent the wheel
import pydotplus as pdp


putorcall = input('Calculate put or call? ')
method = input('Choose method: a) p = 1/2. b) u = 1/d')
diagram = input('Output TikZ diagram (y/n): ')

# input for all constants go here
strike = float(input('Strike price: '))
exptime = int(input('Time to expiry (T): '))
delta = float(input('Step size (delta-t): '))
interest = float(input('Risk free interest (r): '))
sigma = float(input('Volatility (sigma): '))
initprice = float(input('Share value at t=0 (S(0)): '))
dividend = float(input('Continuous dividend yield: '))

steps = int(exptime/delta)
p = 0  # probability. initialised globally cause why not.

# calculates various constants
expfactor = math.exp((interest - dividend) * delta)
cterm = math.pow(0.5 * math.exp(-interest * delta), steps)  # interest is always "r" here, regardless of dividend yield

if method == "a":
    aterm = math.sqrt(math.exp(delta * math.pow(sigma, 2)) - 1)
    d = expfactor * (1 - aterm)
    u = expfactor * (1 + aterm)

if method == "b":
    aterm = 0.5*(math.exp(-(interest-dividend)*delta)+math.exp(((interest-dividend)+math.pow(sigma, 2))*delta))
    d = aterm - math.sqrt(math.pow(aterm, 2)-1)
    u = aterm + math.sqrt(math.pow(aterm,2)-1)
    p = (math.exp((interest-dividend)*delta)-d)/(u-d)


# print('d term is: ', d)
# print('u term is: ', u)

def shareval2(n, m):  # calculates S_n^m, i.e. value of share at step m given n upticks
    return math.pow(d, m-n)*math.pow(u, n)*initprice


sharevalues = np.zeros((steps+1,steps+1))  # initialises a double array for storing share values

outputvalues = input('Print share values S_n^m? (y/n): ')

if outputvalues == "y" or diagram == "y":  # only calculate all values of S if we want a diagram, otherwise only final S
    for m in range(steps+1):
        for n in range(0,m+1):
            sharevalues[n,m] = shareval2(n, m)
            if outputvalues == "y":
                print('S_',n,'^',m,'= ',sharevalues[n,m])


def shareval(i):
    return math.pow(d, steps-i)*math.pow(u, i)*initprice


def putpayoff(i):
    return max(strike-shareval(i), 0)


def callpayoff(i):
    return max(shareval(i)-strike, 0)


def choose(n, k):  # binomial coefficient code
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

# TODO: incorporate optionvals into numpy array


optionvals = []
for x in range(steps+1):
    if putorcall == "put":
        optionvals.insert(x, putpayoff(x))
    if putorcall == "call":
        optionvals.insert(x, callpayoff(x))
    # print('array[',x,']:', optionvals[x])


suma=0

# value the option
if method == "a":
    for x in range(steps+1):
        suma += choose(steps,x)*optionvals[x]
    print('Option value at t=0: ', cterm*suma)
if method == "b":
    for x in range(steps+1):
        suma += choose(steps,x)*math.pow(p,x)*math.pow((1-p),steps-x)*optionvals[x]
    print('Option value at t=0: ', pow(2,steps)*cterm*suma)

# print('u = ', u, ', d = ', d, ', p = ', p, ", A =", aterm)

# Let's generate some diagrams
