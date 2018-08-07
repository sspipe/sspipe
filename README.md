[![Downloads](http://pepy.tech/badge/sspipe)](http://pepy.tech/project/sspipe)
[![Build Status](https://travis-ci.org/sspipe/sspipe.svg?branch=master)](https://travis-ci.org/sspipe/sspipe)
[![PyPI](https://badge.fury.io/py/sspipe.svg)](http://pypi.org/project/sspipe)

# Simple Smart Pipe

SSPipe is a python productivity-tool for rapid data manipulation in python.

It helps you break up any complicated expression into a sequence of
simple transformations, increasing human-readability and decreasing the
need for matching parentheses!

If you're familiar with
[`|` operator](https://en.wikipedia.org/wiki/Pipeline_(Unix))
of Unix, or
[`%>%` operator](https://cran.r-project.org/web/packages/magrittr/vignettes/magrittr.html)
of R's magrittr, or
[`DataFrame.pipe`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.pipe.html)
method of pandas library, `sspipe` provides the same functionality
for any object in python.

### Installation and Usage
Install sspipe using pip:
```bash
pip install --upgrade sspipe
```
Then import it in your scripts.

```python
from sspipe import p
```

Although a few other helper objects are provided, whole functionality
of this library is exposed by `p` object you have imported in
the script above.

### Introduction
Suppose we want to generate a dict, mapping names of 5 biggest
files in current directory to their size in bytes, like below:

`{'README.md': 3732, 'setup.py': 1642, '.gitignore': 1203, 'LICENSE': 1068, 'deploy.sh': 89}`

One approach is to use `os.listdir()` to list files
and directories in current working directory, filter those which are file,
map each to a tuple of (name, size), sort them by size,
take first 5 items, make adict and print it.

Although it is not a good practice to write the whole script in single
expression without introducing intermediary variables, it is an exaggerated
example, doing it in a single expression for demonstration purpose:

```python
import os

print(
    dict(
        sorted(
            map(
                lambda x: [x, os.path.getsize(x)],
                filter(os.path.isfile, os.listdir('.'))
            ), key=lambda x: x[1], reverse=True
        )[:5]
    )
)
```

Using sspipe's `p` operator, the same single expression can be written in a
more human-readable flow of sequential transformations:

```python
import os
from sspipe import p

(
    os.listdir('.')
    | p(filter, os.path.isfile)
    | p(map, lambda x: [x, os.path.getsize(x)])
    | p(sorted, key=lambda x: x[1], reverse=True)[:5]
    | p(dict)
    | p(print)
)
```
As you see, the expression is decomposed into a sequence
starting with initial data, `os.list('.')`, followed by multiple
`| p(...)` stages.

Each `| p(...)` stage describes a transformation that is applied to
 to left-hand-side of `|`.

First argument of `p()` defines the function
 that is applied on data. For example, `x | p(f1) | p(f2) | p(f3)` is
 equivalent to `f3(f2(f1(x)))`.

Rest of arguments of `p()` are passed
 to the transforming function of each stage. For example,
 `x | p(f1, y) | p(f2, k=z)` is equivalent to `f2(f1(x, y), k=z)`


## Advanced Guide

### The `px` helper

TODO: explain.

* `px` is implemented by: `px = p(lambda x: x)`
* `px` is similar to, but not same as, magrittr's dot(`.`) placeholder
  * `x | p(f, px+1, y, px+2)` is equivalent to `f(x+1, y, x+2)`
* `A+1 | f(px, px[2](px.y))` is equivalent to `f(A+1, (A+1)[2]((A+1).y)`
* `px` can be used to prevent adding parentheses
  * `x+1 | px * 2 | np.log(px)+3` is equivalent to: `np.log((x+1) * 2) + 3`

### Integration with Numpy, Pandas, Pytorch

TODO: explain.
* `p` and `px` are compatible with Numpy, Pandas, Pytorch.
* `[1,2] | p(pd.Series) | px[px ** 2 < np.log(px) + 1]` is equivalent to
`x=pd.Series([1, 2]); x[x**2 < np.log(x)+1]`

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

### Internals

TODO: explain.

* `p` is a class that overrides `__ror__` (`|`) operator to apply
the function to operand.

