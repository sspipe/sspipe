<img src="https://sspipe.github.io/img/icon.png" width="120" align="right"/>

[![Downloads](http://pepy.tech/badge/sspipe)](http://pepy.tech/project/sspipe)
[![Build Status](https://travis-ci.org/sspipe/sspipe.svg?branch=master)](https://travis-ci.org/sspipe/sspipe)
[![PyPI](https://badge.fury.io/py/sspipe.svg)](http://pypi.org/project/sspipe)

# Simple Smart Pipe

SSPipe is a python productivity-tool for rapid data manipulation in python.

It helps you break up any complicated expression into a sequence of
simple transformations, increasing human-readability and decreasing the
need for matching parentheses! 

As an example, here is a single line code for reading students' data
from 'data.csv', reporting those in the class 'A19' whose score is more
than the average class score into 'report.csv':

```python
from sspipe import p, px
import pandas as pd

pd.read_csv('data.csv') | px[px['class'] == 'A19'] | px[px.score > px.score.mean()].to_csv('report.csv')
```

As another example, here is a single line code for plotting
sin(x) for points in range(0, 2*pi) where cos(x) is less than 0 in red color:

```python
from sspipe import p, px
import numpy as np
import matplotlib.pyplot as plt

np.linspace(0, 2*np.pi, 100) | px[np.cos(px) < 0] | p(plt.plot, px, np.sin(px), 'r')

# The single-line code above is equivalent to the following code without SSPipe:
# X = np.linspace(0, 2*np.pi, 100)
# X = X[np.cos(X) < 0]
# plt.plot(X, np.sin(X), 'r')
```

If you're familiar with
[`|` operator](https://en.wikipedia.org/wiki/Pipeline_(Unix))
of Unix, or
[`%>%` operator](https://cran.r-project.org/web/packages/magrittr/vignettes/magrittr.html)
of R's magrittr, `sspipe` provides the same functionality in python.

### Installation and Usage
Install sspipe using pip:
```bash
pip install --upgrade sspipe
```
Then import it in your scripts.

```python
from sspipe import p, px
```

The whole functionality
of this library is exposed by two objects `p` (as a wrapper for functions to
be called on the piped object) and `px` (as a placeholder for piped object).

### Examples

| Description | Python expression using `p` and `px` | Equivalent python code |
| --- |:--- |:--- |
| Simple<br>function call | `"hello world!" \| p(print)` | `X = "hello world!"`<br>`print(X)` |
| Function call<br>with extra args | `"hello" \| p(print, "world", end='!')` | `X = "hello"`<br>`print(X, "world", end='!')` |
| Explicitly positioning<br>piped argument<br>with `px` placeholder | `"world" \| p(print, "hello", px, "!")` | `X = "world"`<br>`print("hello", X, "!")` |
| Chaining pipes | `5 \| px + 2 \| px ** 5 + px \| p(print)` | `X = 5`<br>`X = X + 2`<br>`X = X ** 5 + X`<br>`print(X)` |
| Tailored behavior<br>for builtin `map`<br>and `filter` | `(`<br>`  range(5)`<br>`  \| p(filter, px % 2 == 0)`<br>`  \| p(map, px + 10)`<br>`  \| p(list) \| p(print)`<br>`)` | `X = range(5)`<br>`X = filter((lambda x:x%2==0),X)`<br>`X = map((lambda x: x + 10), X)`<br>`X = list(X)`<br>`print(X)` |
| NumPy expressions | `range(10) \| np.sin(px)+1 \| p(plt.plot)` | `X = range(10)`<br>`X = np.sin(X) + 1`<br>`plt.plot(X)` |
| Pandas support | `people_df \| px.loc[px.age > 10, 'name']` | `X = people_df`<br>`X.loc[X.age > 10, 'name']` |
| Assignment | `people_df['name'] \|= px.str.upper()` | `X = people_df['name']`<br>`X = X.str.upper()`<br>`people_df['name'] = X` |
| Pipe as variable | `to_upper = px.strip().upper()`<br>`to_underscore = px.replace(' ', '_')`<br>`normalize = to_upper \| to_underscore`<br>`"  ab cde " \| normalize \| p(print)` | `_f1 = lambda x: x.strip().upper()`<br>`_f2 = lambda x: x.replace(' ','_')`<br>`_f3 = lambda x: _f2(_f1(x))`<br>`X = " ab cde "`<br>`X = _f3(X)`<br>`print(X)` |
| Builtin<br>Data Structures | `2 \| p({px-1: p([px, p((px+1, 4))])})` | `X = 2`<br>`X = {X-1: [X, (X+1, 4)]}` |

### How it works

The expression `p(func, *args, **kwargs)` returns a `Pipe` object that overloads 
`__or__` and `__ror__` operators. This object keeps `func` and `args` and `kwargs` until
evaluation of `x | <Pipe>`, when `Pipe.__ror__` is called by python. Then it will evaluate
`func(x, *args, **kwargs)` and return the result. 

The `px` object is simply `p(lambda x: x)`.

Please notice that SSPipe does not wrap piped objects. On the other hand, it just wraps transforming functions. Therefore, when a variable like `x` is not an instance of `Pipe` class, after python evaluates `y = x | p(func)`, the resulting variable `y` has absolutely no trace of Pipe. Thus, it will be exactly the same object as if we have originally evaluated `y = func(x)`. 

### Common Gotchas

* Incompatibility with `dict.items`, `dict.keys` and `dict.values`:
  
  The objects returned by dict.keys(), dict.values() and dict.items() are
   called [view objects](https://docs.python.org/3.3/library/stdtypes.html#dict-views).
  Python does not allow classes to override the `|` operator on these types. As a workaround,
  the `/` operator has been implemented for view objects. Example:
  ```python3
  # WRONG ERRONEOUS CODE:
  {1: 2, 3: 4}.items() | p(list) | p(print)
  
  # CORRECT CODE (With / operator):
  {1: 2, 3: 4}.items() / p(list) | p(print)
  ```

### Compatibility with JulienPalard/Pipe

This library is inspired by, and depends on, the intelligent and concise work of
 [JulienPalard/Pipe](https://github.com/JulienPalard/Pipe). If you want
 a single `pipe.py` script or a lightweight library that implements core
 functionality and logic of SSPipe, Pipe is perfect.

SSPipe is focused on facilitating usage of pipes, by integration with
 popular libraries and introducing `px` concept and overriding python
 operators to make pipe a first-class citizen.

 Every existing pipe implemented by JulienPalard/Pipe
 library is accessible through `p.<original_name>` and is compatible with SSPipe.
 SSPipe does not implement any specific pipe function and delegates
implementation and naming of pipe functions to JulienPalard/Pipe.

For example, JulienPalard/Pipe's [example](https://github.com/JulienPalard/Pipe#introduction)
for solving "Find the sum of all the even-valued terms in Fibonacci which do not exceed four million."
can be re-written using sspipe:

```python
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from sspipe import p, px

euler2 = (fib() | p.where(lambda x: x % 2 == 0)
                | p.take_while(lambda x: x < 4000000)
                | p.add())
```

You can also pass `px` shorthands to JulienPalard/Pipe API:
```python
euler2 = (fib() | p.where(px % 2 == 0)
                | p.take_while(px < 4000000)
                | p.add())
```
