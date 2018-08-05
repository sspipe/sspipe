# Simple Stupid Pipe

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
                lambda x: (x, os.path.getsize(x)),
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
    | p(map, lambda x: (x, os.path.getsize(x)))
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
 `x | p(f1, y) | p(f2, k=z)` is equivalent to `f2(f1(y, x), k=z)`


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

### Integration with PyToolz

TODO: explain.

[PyToolz](https://github.com/pytoolz/toolz) provides a set of utility
functions for iterators, functions, and dictionaries. For each utility
function `f()` which is provided by pytoolz, `p.f()` is piped version
of that utility.

* `{'x': 1, 'y': 7} | p.valmap(px+1)` equals `{'x': 2, 'y': 8}`
* `range(5) | p.map(px**2) | p(list)` equals `[0, 1, 4, 9, 16]`


### Internals

TODO: explain.

* `p` is a class that overrides `__ror__` (`|`) operator to apply
the function to operand.


