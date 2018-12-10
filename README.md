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
df = pd.DataFrame([np.random.uniform(10,1,size=1000),
                   np.random.uniform(10,5,size=1000),
                   np.random.randint(1,high=10,size=1000),
                   np.random.choice(list('ABCD'),size=1000)],
                  index=['col1','col2','col3','col4']).T
```

# line

![line_figure](./img/line_figure.png)

# bar

![](./img/bar_figure.png)

# histogram

![](./img/histogram_figure.png)

# scatter

![](./img/scatter_category_figure.png)

![](./img/scatter3d_category_figure.png)



# pie

![](./img/pie_figure.png)

# rose pie

![](./img/pie_rose_figure.png)

# countplot

![](./img/countplot_figure.png)

# box

![](./img/box_figure.png)

![](./img/box_series_figure.png)

More examples can be found in the notebook `eplot useage example.ipynb`.