import pandas
import pyecharts
import numpy as np
from pandas.core.base import PandasObject
from pandas.core.accessor import CachedAccessor

def bar(data,title=None,useCols=None,**args):
    if isinstance(data,pandas.Series):
        barFig = pyecharts.Bar(title)
        barFig.add(data.name,data.index,data.values,is_label_show=True,**args)
        return barFig
    elif isinstance(data,pandas.DataFrame):
        useCols = useCols if useCols else data.columns
        bar = pyecharts.Bar(title)
        for i in useCols:
            barFig.add(i,data.index,data[i],bar_category_gap=0,is_label_show=True,**args)
        return barFIg
def line(data,title=None, lineConfig = None, manylineConfig=None,useCols=None,**args):
    
    if isinstance(data,pandas.Series):
        lineConfig  = lineConfig if lineConfig else {}
        lineFig = pyecharts.Line(title)
        lineFig.add(data.name,data.index,data.values,**lineConfig,**args)
        return lineFig
    if useCols is None:
        useCols = data.columns    
    lineFig = pyecharts.Line(title)
    if lineConfig is None:
        manyLineConfig = {}
    for i in useCols:    
        lineFig.add(i, data.index, data[i],**manyLineConfig.get(i,{}))#, mark_point=["average"])    
    return lineFig

def pie(data,y=None,title=None,**args):
    pieFig = pyecharts.Pie(title)
    if isinstance(data, pandas.Series):        
        pieFig.add(data.name,data.index,data.values,**args)
    elif isinstance(data, pandas.DataFrame):
        pieFig.add(y,data.index,data[y].values,**args)
    return pieFig
def hist(data,title= 'histogram',bins = 10,**args):
    histFig = pyecharts.Bar(title)
    y,x = np.histogram(data,bins=bins)
    x = x.astype(int).astype(str)
    xlabels = [x[i-1]+'-'+x[i] for i in range(1,len(x))]
    histFig.add(data.name,xlabels,y, bar_category_gap=1,is_label_show=True,**args)
    return histFig

def box(data,title=None,**args):
    boxFig = pyecharts.Boxplot(title)
    if isinstance(data,pandas.Series):
        boxFig.add('',[data.name],boxFig.prepare_data(data.values.reshape(1,-1)),**args)
        return boxFig
    elif isinstance(data,pandas.DataFrame):
        boxFig.add('',data.columns,boxFig.prepare_data(data.T.values),xaxis_interval=0,**args)
        return boxFig
def countplot(data,title=None,**args):
    return data.value_counts().eplot.bar(title='countplot',**args)

def eplot_series(se,kind='bar',**kwds):
    if kind == 'bar':
        return bar(se,**kwds)
    if kind == 'line':
        return line(se,**kwds)
    if kind == 'pie':
        return pie(se,**kwds)
    if kind == 'hist':
        return hist(se,**kwds)
    if kind == 'box':
        return box(se,**kwds)
    if kind == 'countplot':
        return countplot(se,**kwds)
    
def eplot_frame(df,kind='bar',x=None,y=None,**kwds):
    if kind == 'bar':
        return bar(df,**kwds)
    if kind == 'line':
        return line(df,**kwds)
    if kind == 'box':
        return box(df,**kwds)
    if kind == 'pie':
        return pie(df,y=y,**kwds)

class EchartsBasePlotMethods(PandasObject):
    def __init__(self, data):
        self._parent = data  # can be Series or DataFrame
    def __call__(self, *args, **kwargs):
        raise NotImplementedError
        
class EchartsSeriesPlotMethods(EchartsBasePlotMethods):
    def __call__(self,kind='line',**kwds):
        return eplot_series(self._parent,kind=kind,**kwds)
    def bar(self,**kwds):
        return self(kind='bar',**kwds)
    def line(self,**kwds):
        return self(kind='line',**kwds)
    def pie(self,title='pie',legend_orient="vertical",is_label_show = True, legend_pos="left",inner_radius_from = 0,**kwds):
        kwds.update({'legend_orient':legend_orient})
        kwds.update({'legend_pos':legend_pos})
        kwds.update({'radius':[inner_radius_from,75]}) 
        kwds.update({'is_label_show':is_label_show})
        return self(kind='pie',**kwds)
    def hist(self,title= 'histogram',bins = 10,**kwds):
        return self(kind='hist',**kwds)
    def box(self,title='box',**kwds):
        return self(kind='box',**kwds)
    def countplot(self,title='countplot',**kwds):
        return self(kind='countplot',**kwds)
    
    
class EchartsFramePlotMethods(EchartsBasePlotMethods):
    def __call__(self,kind='line',x=None,y=None,**kwds):
        return eplot_frame(self._parent,kind=kind,x=None,y=y,**kwds)
    def bar(self,**kwds):
        return self(kind='bar',**kwds)
    def line(self,**kwds):
        return self(kind='line',**kwds)
    def box(self,title='box',**kwds):
        return self(kind='box',**kwds)
    def pie(self,title='pie',y=None,legend_orient="vertical",is_label_show = True, legend_pos="left",inner_radius_from = 0,**kwds):
        kwds.update({'legend_orient':legend_orient})
        kwds.update({'legend_pos':legend_pos})
        kwds.update({'radius':[inner_radius_from,75]}) 
        kwds.update({'is_label_show':is_label_show})
        return self(kind='pie',y=y,**kwds)    

pandas.Series.eplot = CachedAccessor("eplot",EchartsSeriesPlotMethods)
pandas.DataFrame.eplot = CachedAccessor("eplot",EchartsFramePlotMethods)
