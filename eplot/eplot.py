import pandas
import pyecharts
import numpy as np
from pandas.core.base import PandasObject
from pandas.core.accessor import CachedAccessor
import pyecharts.options as opts
from pyecharts.render.display import HTML
from pyecharts.render.engine import RenderEngine
from pyecharts.commons import utils

Config = {'return_type': 'HTML'}


def set_config(**kwargs):
    '''
  if return type is HTML, you can see the chart directly in jupyter notebook, but cannot change anymore
  if return type is CHART, you need `df.col1.eplot.bar().render_notebook()`  in order to display in notebook.
  '''
    global Config
    for i in kwargs.keys():
        Config[i] = kwargs[i]


def bar(data, title=None, useCols=None, **args):
    barFig = pyecharts.charts.Bar()
    barFig.set_global_opts(title_opts=opts.TitleOpts(title=title))
    if isinstance(data, pandas.Series):
        barFig.add_xaxis(data.index.tolist())
        barFig.add_yaxis(data.name, data.values.tolist())
    elif isinstance(data, pandas.DataFrame):
        useCols = useCols if useCols else data.columns
        for i in useCols:
            barFig.add_xaxis(data[i].index.tolist())
            barFig.add_yaxis(i, data[i].values.tolist())
    result = barFig.render_notebook(
    ) if Config['return_type'] == 'HTML' else barFig
    return result


def line(
        data,
        title=None,
        lineConfig=None,
        manyLineConfig=None,
        useCols=None,
        **args):
    lineFig = pyecharts.charts.Line()
    lineFig.set_global_opts(title_opts=opts.TitleOpts(title=title))
    if isinstance(data, pandas.Series):
        lineConfig = lineConfig if lineConfig else {}

        lineFig.add_xaxis(data.index.tolist())
        lineFig.add_yaxis(data.name, data.values.tolist(),
                          **lineConfig, **args)
    elif isinstance(data, pandas.DataFrame):
        if useCols is None:
            useCols = data.columns
        if lineConfig is None:
            manyLineConfig = {}
        for i in useCols:
            lineFig.add_xaxis(data.index.tolist())\
                .add_yaxis(i, data[i].tolist(), **manyLineConfig.get(i, {}))
    lineFig.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    result = lineFig.render_notebook(
    ) if Config['return_type'] == 'HTML' else lineFig
    return result


def pie(data, y=None, title=None, **args):
    pieFig = pyecharts.charts.Pie()
    pieFig.set_global_opts(title_opts=opts.TitleOpts(title=title))
    if isinstance(data, pandas.Series):
        pieFig.add(data.name, list(zip(data.index.tolist(),
                                       data.values.tolist())), **args)
    elif isinstance(data, pandas.DataFrame):
        pieFig.add(y, list(zip(data.index.tolist(),
                               data[y].values.tolist())), **args)
    pieFig.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    result = pieFig.render_notebook(
    ) if Config['return_type'] == 'HTML' else pieFig
    return result


def hist(data, title='histogram', bins=10, **args):
    histFig = pyecharts.charts.Bar()
    histFig.set_global_opts(title_opts=opts.TitleOpts(title=title))
    y, x = np.histogram(data, bins=bins)
    x = x.astype(int).astype(str)
    xlabels = [x[i - 1] + '-' + x[i] for i in range(1, len(x))]
    histFig.add_xaxis(xlabels)
    histFig.add_yaxis(data.name, y.tolist(), **args)
    result = histFig.render_notebook(
    ) if Config['return_type'] == 'HTML' else histFig
    return result


def box(data, title=None, **args):
    boxFig = pyecharts.charts.Boxplot()
    boxFig.set_global_opts(title_opts=opts.TitleOpts(title=title))
    if isinstance(data, pandas.Series):
        boxFig.add_xaxis([data.name])
        boxFig.add_yaxis('', boxFig.prepare_data(
            data.values.reshape((1, -1)).tolist()))
    elif isinstance(data, pandas.DataFrame):
        boxFig.add_xaxis(data.columns.tolist())
        boxFig.add_yaxis('', boxFig.prepare_data(data.values.T.tolist()))
    result = boxFig.render_notebook(
    ) if Config['return_type'] == 'HTML' else boxFig
    return result


def countplot(data, title=None, **args):
    return data.value_counts().eplot.bar(title='countplot', **args)


def scatter(
        data,
        x,
        y,
        category_col=None,
        title=None,
        category_name=None,
        **args):
    scatterFig = pyecharts.charts.Scatter()
    lineFig = pyecharts.charts.Line()
    scatterFig.set_global_opts(title_opts=opts.TitleOpts(title=title))
    if category_col is None:
        (scatterFig.add_xaxis(data[x].values.tolist())
         .add_yaxis('', df[y].values.tolist())
         .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
         )
    else:
        for cat, d in data.groupby(category_col):
            #scatterFig.add(cat, d[x], d[y], **args)
            (scatterFig.add_xaxis(d[x].values.tolist())
             .add_yaxis(cat, d[y].values.tolist())
             .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
             )
    result = scatterFig.render_notebook(
    ) if Config['return_type'] == 'HTML' else scatterFig
    return result


def scatter3d(
        data,
        x,
        y,
        z,
        category_col=None,
        title=None,
        category_name=None,
        **args):
    scatter3dFig = pyecharts.charts.Scatter3D(title)
    if category_col is None:
        scatter3dFig.add(category_name, data[[x, y, z]].values, **args)
    else:
        for cat, d in data.groupby(category_col):
            scatter3dFig.add(cat, d[[x, y, z]].values, **args)
    result = scatter3dFig.render_notebook(
    ) if Config['return_type'] == 'HTML' else scatter3dFig
    return result


def eplot_series(se, kind='bar', title=None, bins=10, **kwds):
    if kind == 'bar':
        return bar(se, title=title, **kwds)
    if kind == 'line':
        return line(se, title=title, **kwds)
    if kind == 'pie':
        return pie(se, title=title, **kwds)
    if kind == 'hist':
        return hist(se, title=title, bins=bins, **kwds)
    if kind == 'box':
        return box(se, title=title, **kwds)
    if kind == 'countplot':
        return countplot(se, title=title, **kwds)


def eplot_frame(
        df,
        kind='bar',
        x=None,
        y=None,
        z=None,
        category_col=None,
        category_name=None,
        title=None,
        **kwds):
    if kind == 'bar':
        return bar(df, title=title, **kwds)
    if kind == 'line':
        return line(df, title=title, **kwds)
    if kind == 'box':
        return box(df, title=title, **kwds)
    if kind == 'pie':
        return pie(df, y=y, title=title, **kwds)
    if kind == 'scatter':
        return scatter(
            df,
            x=x,
            y=y,
            category_col=category_col,
            category_name=category_name,
            title=title,
            **kwds)
    if kind == 'scatter3d':
        return scatter3d(
            df,
            x=x,
            y=y,
            z=z,
            category_col=category_col,
            category_name=category_name,
            title=title,
            **kwds)


class EchartsBasePlotMethods(PandasObject):
    def __init__(self, data):
        self._parent = data  # can be Series or DataFrame

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class EchartsSeriesPlotMethods(EchartsBasePlotMethods):
    def __call__(self, kind='line', bins=10, title=None, **kwds):
        return eplot_series(
            self._parent,
            kind=kind,
            title=title,
            bins=bins,
            **kwds)

    def bar(self, title='bar', **kwds):
        return self(kind='bar', title=title, **kwds)

    def line(self, title='line', **kwds):
        return self(kind='line', title=title, **kwds)

    def pie(
            self,
            title='pie',
            y=None,
            color=None,
            radius=None,
            center=None,
            rosetype=None,
            label_opts=None,
            **kwds):
        if color is not None:
            kwds.update({'color': color})
        if radius is not None:
            kwds.update({'radius': radius})
        if center is not None:
            kwds.update({'center': center})
        if rosetype is not None:
            kwds.update({'rosetype': rosetype})
        if label_opts is not None:
            kwds.update({'label_opts': label_opts})
        return self(kind='pie', title=title, **kwds)

    def hist(self, title='histogram', bins=10, **kwds):
        return self(kind='hist', title=title, bins=bins, **kwds)

    def box(self, title='box', **kwds):
        return self(kind='box', title=title, **kwds)

    def countplot(self, title='countplot', **kwds):
        return self(kind='countplot', title=title, **kwds)


class EchartsFramePlotMethods(EchartsBasePlotMethods):
    def __call__(
            self,
            kind='line',
            x=None,
            y=None,
            z=None,
            category_col=None,
            category_name=None,
            title=None,
            **kwds):
        return eplot_frame(
            self._parent,
            kind=kind,
            x=x,
            y=y,
            z=z,
            category_col=category_col,
            category_name=category_name,
            title=title,
            **kwds)

    def bar(self, title='bar', **kwds):
        return self(kind='bar', title=title, **kwds)

    def line(self, title='line', **kwds):
        return self(kind='line', title='title', **kwds)

    def box(self, title='box', **kwds):
        return self(kind='box', title=title, **kwds)

    def pie(
            self,
            title='pie',
            y=None,
            color=None,
            radius=None,
            center=None,
            rosetype=None,
            label_opts=None,
            **kwds):
        if color is not None:
            kwds.update({'color': color})
        if radius is not None:
            kwds.update({'radius': radius})
        if center is not None:
            kwds.update({'center': center})
        if rosetype is not None:
            kwds.update({'rosetype': rosetype})
        if label_opts is not None:
            kwds.update({'label_opts': label_opts})
        return self(kind='pie', y=y, title=title, **kwds)

    def scatter(
            self,
            x,
            y,
            category_col=None,
            category_name=None,
            title='scatter'):
        return self(
            kind='scatter',
            x=x,
            y=y,
            category_col=category_col,
            category_name=category_name,
            title=title)

    def scatter3d(
            self,
            x,
            y,
            z,
            category_col=None,
            category_name=None,
            title='scatter3d'):
        return self(
            kind='scatter3d',
            x=x,
            y=y,
            z=z,
            category_col=category_col,
            category_name=category_name,
            title=title)


pandas.Series.eplot = CachedAccessor("eplot", EchartsSeriesPlotMethods)
pandas.DataFrame.eplot = CachedAccessor("eplot", EchartsFramePlotMethods)
