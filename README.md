# `eplot
pandas interface for pyecharts

pyecharts is a great python module as a wrapper for echarts, it is also simple to use in pandas by function `add` .

http://pyecharts.org/#/zh-cn/prepare

However, it will be more simple if it can use as 

Impired by `cufflinks` to `plotly`, I create this codes for the smoothly useage in `pandas` , by only add functions to the `DataFrame` or `Series` object. Thus we need not to call pyecharts  or creat pyecharts objects out of the `DataFrame`

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

