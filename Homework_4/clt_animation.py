import numpy as np

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import time

import sqlite3

import seaborn as sns

from matplotlib.pylab import *
import matplotlib.animation as animation

from scipy import stats 

connection = sqlite3.connect('data_db.db')
c = connection.cursor()

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 3)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])
ax5 = fig.add_subplot(gs[:, 2])

def animate(i):
    
    query = ('SELECT * FROM CLT_data2')
    data1 = pd.read_sql_query(query, connection)
    x1 = data1.mean_values
    ax1.cla()
    ax1.hist(x1)
    ax1.set_title("Distribution of Means", size = 12)
    

    query = ('SELECT * FROM CLT_data2')
    data2 = pd.read_sql_query(query, connection)
    x2 = data1.mean_values
    ax2.cla()
    stats.probplot(x2, dist = "norm", plot = ax2)

    query = ('SELECT * FROM CLT_data2')
    data3 = pd.read_sql_query(query, connection)
    x3 = data3.pvalues.values
    ax3.cla()
    ax3.text(0.01, 0.5, f"P values: {x3[-1]}")
    ax3.set_title("Normality test P-value", size = 12)
    ax3.axes.xaxis.set_visible(False)
    ax3.axes.yaxis.set_visible(False)

    query = ('SELECT * FROM CLT_data2')
    data4 = pd.read_sql_query(query, connection)
    x4 = data4.pvalues
    ax4.cla()
    ax4.plot(x4)
    ax4.set_title("Historical P-values", size = 12)
    
    query = ('SELECT * FROM CLT_data1')
    data5 = pd.read_sql_query(query, connection)
    x5 = data5.outputs
    ax5.cla()
    sns.countplot(x=x5, data=data5, ax = ax5, color=sns.color_palette()[0])
    ax5.set_title("Distribution of Outputs", size = 12)
    

ani = FuncAnimation(plt.gcf(), animate, interval = 500)
plt.show()