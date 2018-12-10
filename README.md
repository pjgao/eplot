# eplot

`eplot` is a `pandas` interface for `pyecharts`.

As we know, `pyecharts` is a great python module as a wrapper for echarts, it is  easy to use in `pandas` by function `add` .

http://pyecharts.org/#/zh-cn/prepare

However, it will be more simple if it can be used as raw `pandas`  plot module, eg: `df.plot.bar()`.

Impired by `cufflinks` to `plotly`, I created these codes for the `pyecharts` smoothly useage in `pandas` , by only registering functions to the `DataFrame` or `Series` classes. 

As a result, we need not to call pyecharts  or creat pyecharts objects out of the `DataFrame`, we plot interacted figures in the `pyecharts` backend only in one line as follow:

Useage:

```python
import eplot
import pandas as pd
import numpy as np
se = pd.Series(np.random.randint(10,size=100))
df = pd.DataFrame({'mass': [0.330, 4.87 , 5.97],'radius': [2439.7, 6051.8, 6378.1]}, index=['Mercury', 'Venus', 'Earth'])
df.eplot()
```

```python
df.eplot.pie(y='mass')
```

```python
se.eplot.countplot()
```

```python
se.eplot.box()
```

More examples can be found in the notebook `eplot useage example.ipynb`.