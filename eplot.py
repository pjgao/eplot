#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:  pjgao
@city: Nanjing
"""


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
        barFig = pyecharts.Bar(title)
        for i in useCols:
            barFig.add(i,data.index,data[i],is_label_show=True,**args)
        return barFig

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
    
def scatter(data,x,y,category_col=None,title=None,category_name = None, **args):
    scatterFig = pyecharts.Scatter(title)
    if category_col is None:
        scatterFig.add(category_name,data[x],data[y],**args)
    else:
        for cat,d in data.groupby(category_col):
            scatterFig.add(cat,d[x],d[y],**args)
    return scatterFig

def scatter3d(data,x,y,z,category_col=None,title=None,category_name = None, **args):
    scatter3dFig = pyecharts.Scatter3D(title)
    if category_col is None:        
        scatter3dFig.add(category_name,data[[x,y,z]].values,**args)
    else:
        for cat,d in data.groupby(category_col):
            scatter3dFig.add(cat,d[[x,y,z]].values,**args)
    return scatter3dFig            

def eplot_series(se,kind='bar',title=None,bins=10,**kwds):
    if kind == 'bar':
        return bar(se,title=title,**kwds)
    if kind == 'line':
        return line(se,title=title,**kwds)
    if kind == 'pie':
        return pie(se,title=title,**kwds)
    if kind == 'hist':
        return hist(se,title=title,bins=bins,**kwds)
    if kind == 'box':
        return box(se,title=title,**kwds)
    if kind == 'countplot':
        return countplot(se,title=title,**kwds)
    
def eplot_frame(df,kind='bar',x=None,y=None, z=None, category_col=None,category_name=None,title=None,**kwds):
    if kind == 'bar':
        return bar(df,title=title,**kwds)
    if kind == 'line':
        return line(df,title=title,**kwds)
    if kind == 'box':
        return box(df,title=title,**kwds)
    if kind == 'pie':
        return pie(df,y=y,title=title,**kwds)
    if kind == 'scatter':
        return scatter(df,x=x,y=y,category_col=category_col,category_name=category_name,title=title,**kwds)
    if kind == 'scatter3d':
        return scatter3d(df,x=x,y=y,z=z,category_col=category_col,category_name=category_name,title=title,**kwds)

        
class EchartsBasePlotMethods(PandasObject):
    def __init__(self, data):
        self._parent = data  # can be Series or DataFrame
    def __call__(self, *args, **kwargs):
        raise NotImplementedError
        
class EchartsSeriesPlotMethods(EchartsBasePlotMethods):
    def __call__(self,kind='line',bins=10,title=None,**kwds):        
        return eplot_series(self._parent,kind=kind,title=title,bins=bins,**kwds)
    def bar(self,title='bar',**kwds):
        return self(kind='bar',title=title,**kwds)
    def line(self,title='line',**kwds):
        return self(kind='line',title=title,**kwds)
    def pie(self,title='pie',legend_orient="vertical",rosetype=None,is_label_show = True, is_legend_show=True,legend_pos="right",inner_radius_from = 0,**kwds):
        if rosetype is not None:
            kwds.update({'rosetype':rosetype})
        kwds.update({'legend_orient':legend_orient})
        kwds.update({'legend_pos':legend_pos})
        kwds.update({'radius':[inner_radius_from,75]}) 
        kwds.update({'is_label_show':is_label_show})
        kwds.update({'is_legend_show':is_legend_show})
        return self(kind='pie',title=title,**kwds)
    def hist(self,title= 'histogram',bins = 10,**kwds):
        return self(kind='hist',title=title,bins=bins,**kwds)
    def box(self,title='box',**kwds):
        return self(kind='box',title=title,**kwds)
    def countplot(self,title='countplot',**kwds):
        return self(kind='countplot',title=title,**kwds)
    
class EchartsFramePlotMethods(EchartsBasePlotMethods):
    def __call__(self,kind='line',x=None,y=None,z=None,category_col=None,category_name=None,title=None,**kwds):
        return eplot_frame(self._parent,kind=kind,x=x,y=y,z=z,category_col=category_col,category_name=category_name,title=title,**kwds)
        
    def bar(self,title='bar',**kwds):
        return self(kind='bar',title=title,**kwds)
        
    def line(self,title='line',**kwds):
        return self(kind='line',title='title',**kwds)
        
    def box(self,title='box',**kwds):
        return self(kind='box',title=title,**kwds)
        
    def pie(self,title='pie',y=None,legend_orient="vertical",rosetype=None,is_label_show = True,is_legend_show=True, legend_pos="right",inner_radius_from = 0,**kwds):
        if rosetype is not None:
            kwds.update({'rosetype':rosetype})
        kwds.update({'legend_orient':legend_orient})
        kwds.update({'legend_pos':legend_pos})
        kwds.update({'radius':[inner_radius_from,75]}) 
        kwds.update({'is_label_show':is_label_show})
        kwds.update({'is_legend_show':is_legend_show})
        return self(kind='pie',y=y,title=title,**kwds)    
        
    def scatter(self,x,y,category_col=None,category_name=None,title='scatter'):
        return self(kind='scatter',x=x,y=y,category_col=category_col,category_name=category_name,title=title)
        
    def scatter3d(self,x,y,z,category_col=None,category_name=None,title='scatter3d'):
        return self(kind='scatter3d',x=x,y=y,z=z,category_col=category_col,category_name=category_name,title=title)
        
        
pandas.Series.eplot = CachedAccessor("eplot",EchartsSeriesPlotMethods)
pandas.DataFrame.eplot = CachedAccessor("eplot",EchartsFramePlotMethods)
