# Python
- Numpy Financial (2021.11.08)


## Numpy Financial : TVM (2021.11.08)

- **TVM** : `PV` `FV` `FMT` `NPV` and `IRR`
- Documentation ☞ https://numpy.org/numpy-financial/latest

```python
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
```

> -10000.0  
> 12100.0  
> 1627.4539  
> -0.0  
> 0.1