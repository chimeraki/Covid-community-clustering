import pandas as pd
import numpy as np
import scipy.stats as ss
#Converting to weights
filen="EdgeList.dat"
rt=pd.read_csv(filen)

weights=rt.n/rt.n.max()


#Dictionary from names to ISO3

filen="countries_codes_and_coordinates.csv"
ccode=pd.read_csv(filen)
c_iso3=dict(zip(ccode.Country,ccode.Alpha3Code))


#Writing weights to a file
c1=[]
c2=[]
fout=open("Weights.dat","w")
fout.write("C1\tC2\twt\n")
for i in range (0,len(weights)):
	c1.append(c_iso3[rt.country_x[i]][2:-1])
	c2.append(c_iso3[rt.country_y[i]][2:-1])
	fout.write(c1[i]+'\t'+c2[i]+'\t'+str(weights[i])+'\n')
fout.close()

wtlist=zip(c1,c2,weights)

##########Created by: Sanjukta Krishnagopal#########
##################April 2020#######################


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

N=np.shape(S)[0]
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

# Countries, and weights
#SVG April 2020
countilist=[]
countjlist=[]
edge_w=[]
edge_c=[]
for i in range(N):
    for j in range(i):
		countilist.append(count[i])
		countjlist.append(count[j])
		edge_w.append(np.linalg.norm(dic[count[i]]-dic[count[j]])) #Similarity Weights
		edge_c.append(ss.spearmanr(dic[count[i]],dic[count[j]])[0])#Correlation Coeff
##SVG April 2020
edge_w=edge_w/max(edge_w)

airsubset_w=[]

print(countilist[1])
print(wtlist[1][0])
for i in range (0, len(countilist)):
	for j in range (0, len(wtlist)):
		
		if(wtlist[j][0]==countilist[i])and(wtlist[j][1]==countjlist[i]):	
			
			airsubset_w.append(wtlist[i][2])
			break
	if(j==len(wtlist)-1):
		print(wtlist[j][0],countilist[i],wtlist[j][1],countjlist[i]) # Countries with no direct flights
		airsubset_w.append(0.0)
airsubset_w=airsubset_w/max(airsubset_w)

fout=open("junk.dat","w")
for i in range (0,len(edge_w)):
	fout.write(str(airsubset_w[i])+'\t'+str(edge_c[i])+'\n')
fout.close()

print(ss.spearmanr(airsubset_w,edge_w))
