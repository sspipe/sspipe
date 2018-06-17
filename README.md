# Stupid Simple Pipe

`pip install sspipe` then:

* `x | p(f)` is equal to `f(x)`
* `x | p(f).attr[item](arg) + 2 | p(g)` is equal to `g( f(x).attr[item](arg) + 2 )`
* `(x | p(f)) | p(g)` is equal to `x | (p(f) | p(g))`
* `px` is equal to `p(lambda x: x)`

Now, instead of

```python
from pathlib import Path

print(' '.join(list(map(str, filter((lambda x: x.is_dir()), Path('/etc').glob('*'))))))
```

Write:

```python
from sspipe import p, px
from pathlib import Path

Path('/etc').glob('*') | p.filter(px.is_dir()) | p.map(str) | p(list) | p(' '.join) | p(print)
```
