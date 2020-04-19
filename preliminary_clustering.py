##########Covid: Country Similarity for Covid ############
##########Created by: Sanjukta Krishnagopal#########
##################April 2020#######################

from numpy import *
from matplotlib.pyplot import *
import random
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import pandas as pd
from scipy.spatial.distance import cdist
import community
import igraph

matplotlib.rc('xtick', labelsize=13) 
matplotlib.rc('ytick', labelsize=13)

def mse(Y, YH):
     return np.square(Y - YH).mean()

def nor(Y):
     return np.square(Y).mean()

path = 'World_cases.csv'
df_conf = pd.read_csv(path).values

#delete NZ and TUR with blank data and countries with very few days of data
S=np.delete(df_conf,[7,10,15],axis=0) 
count=list(S[:,0])
S=S[:,1:]

#removing zeros in data and converting all data in equal length

N=shape(S)[0]
dic={}
l=[]
for i in range(N):
    start=np.where(S[i] > 0)[0][0]
    dic[count[i]]=S[i,start:].astype(float)
    l.append(len(S[i,start:]))
      
min_l=min(l)
for i in range(N):
    v=dic[count[i]]
    v=v[:min_l]
    v[np.isnan(v)]=0
    dic[count[i]]=v

# adjacency matrix using l2 norm

A=np.zeros((N,N))
for i in range(N):
    A[i,i]=0
    for j in range(i):
        A[i,j]= A[j,i]=linalg.norm(dic[count[i]]-dic[count[j]])

A=1-A/np.max(A)

# Louvain community detection

H=nx.Graph(A)              
part = community.best_partition(H)
values = [part.get(node) for node in H.nodes()]
mod = community.modularity(part,H)

nocomm=len(np.unique(values))
country_comm = dict(zip(count, values))

#plotting

figure()
mapping=dict(zip(H,count))
H = nx.relabel_nodes(H, mapping)
nx.draw_spring(H, cmap = plt.get_cmap('jet'), node_color = values, node_size=100,with_labels=True, width = 0.1)
savefig('plot.pdf')
