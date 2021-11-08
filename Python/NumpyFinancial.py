# Practice : Numpy Financial
# Documentation ☞ https://numpy.org/numpy-financial/latest


import numpy_financial as npf

# pv(rate, nper, pmt, fv=0, when='end')
pv = npf.pv(0.1, 2, 0, 12100)
print(round(pv, 4))

# fv(rate, nper, pmt, pv, when='end')
fv = npf.fv(0.1, 2, 0, -10000)
print(round(fv, 4))

# pmt(rate, nper, pv, fv=0, when='end')
pmt = npf.pmt(0.1, 10, -10000)
print(round(pmt, 4))

# npv(rate, values)
npv = npf.npv(0.1, [-10000, +1000, +1000, +11000])
print(round(npv, 4))

# irr(values)
irr = npf.irr([-10000, 1000, 1000, 11000])
print(round(irr, 4))