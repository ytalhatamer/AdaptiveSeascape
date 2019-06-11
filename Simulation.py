#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 12:17:39 2018

@author: ytalhatamerlab
"""
import sys
blockme=int(sys.argv[1])
startwith=int(sys.argv[2])
simtype=int(sys.argv[3])
if simtype==0:
    simmodes=[0]
elif simtype==1:
    simmodes=[1]
elif simtype==2:
    simmodes=range(2)
import pickle,time
import pandas as pd
from datetime import datetime as dtdt
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import numpy as np
import sqlite3 as sq
global graph,Km,Ki,kcat,graphrowlen, fitthr, promoter_effect,maxTMP,graphcols
from random import randint
maxTMP=10333425# in log(maxTMP) since we use this number in below line (in logspace function)
                        # Highest soluble TMP in M9 media is set as 3g/L=10333 uM
                        # We send TMP concentration to V function as nanomolar
                        # thus we need to set highest TMP concentration as 10,333,425nM
graph=pickle.load(open('../dhfrgraph2d.pickle','rb'))
nowheader=str(dtdt.now()).replace('-','_').replace(' ','_').replace(':','_').replace('.','_')[0:19]
Data=pd.ExcelFile('../../GrowthRate_BiochemicalData.xlsx').parse('Simulations').as_matrix() # Load Data file
Km=[i[0] for i in Data]     #Km values from data chart
kcat=[i[1] for i in Data]   #kcat values from data chart
Ki=[i[2] for i in Data]    #Ki values from data chart
linecolors=['blue',[0,1,0],[0,.47,0],'magenta','cyan','red',[.67,.67,.67]]
rowlen=[5,6] # Graph Row Length for adding promoter mutation or not...
promoter_effect=10
zipicklefolder='Results/'

graphcols=[1,2,4,6,12,24,100]
def parsefilename(filename):
    if filename[-7:]=='.pickle':
        name=filename[:-7]
    params,date_times=name.split('-')
    timesrun=date_times.split('_')[1]
    date='_'.join(date_times.split('_')[2:])
    
    startwith,fitpct,prom=params.split('_')
    startwith=int(startwith[2:])
    fitpct=float(fitpct[2:])
    if prom=='WP':
        promoter=1
    elif prom=='NP':
        promoter=0
    return startwith,fitpct,promoter,date,timesrun,name

def calculateV(tmp):
        E=np.ones(148)
        Subs=12.5  #uM
        v=np.ones(148)
        for i in range(148):
            if i<48:
                E[i]=.02
                v[i]=(kcat[i]/Km[i])*(E[i]*Subs)/(1+(tmp/Ki[i])+(Subs/Km[i]))
            elif i<100 and i>=48:
                E[i]=np.NaN
                v[i]=np.NaN
            else:
                E[i]=.02*promoter_effect
                v[i]=(kcat[i-100]/Km[i-100])*(E[i]*Subs)/(1+(tmp/Ki[i-100])+(Subs/Km[i-100]))
        return(v)
    
def findmic(mutant,fitthr):
    vWT_max=calculateV(0)[0]
    V_thr=vWT_max*fitthr
    S=12.5  #uM
    if mutant<48:
        E=.02
    elif mutant<100 and mutant>=48:
        E=np.NaN
    else:
        E=.02*promoter_effect
        mutant-=100

    inhconc=Ki[mutant]*(((kcat[mutant]*E*S)/(V_thr*Km[mutant]))-1-(S/Km[mutant]))
    return inhconc

def pack_results(data):
    traj={}
    for res in data:
        s=tuple(res[0])
        if s in traj:
            traj[s][2]+=1
        else:
            traj[s]=[res[1],res[2],1]
    return traj

def zipickle(data,folder,filename):
    start=time.time()
    _,_,_,_,_,name=parsefilename(filename)
    pickle.dump(data,open(folder+name+'.zipickle','wb'))
    end=time.time()
    print ('Pickling Time: ',end-start)

def export_db(data,folder,filename):

    start=time.time()
    startwith,fitpct,promoter,date,timesrun,name=parsefilename(filename)
    #fitthr=.1459*fitpct # WT Vmax =0.1459 ([TMP]=0 uM)
    fitpct*=100
    errorrate=0
    con=sq.connect(folder+name+'.db')
    with con:
        cur=con.cursor()
        cur.execute("DROP TABLE IF EXISTS parameters")
        cur.execute("DROP TABLE IF EXISTS results")
        cur.execute("CREATE TABLE parameters(DateTime DATETIME,Number_of_Simulation INT, PromoterPresent INT, FitnessThreshold REAL, FitnessPercent REAL, ErrorRate REAL)")
        cur.execute("INSERT INTO parameters VALUES(?,?,?,?,?,?)",(date,timesrun,promoter,fitthr,fitpct,errorrate))
        cmd='CREATE TABLE results(Trajectory TEXT,Times_Seen INT, TMP_Reached REAL, ReachedMAX INT, Dead_On INT, PATH TEXT);'
        cur.execute(cmd)
        cmd2='INSERT INTO results VALUES(?,?,?,?,?,?)'
        for i in range(len(data)):
            mykey=list(data.keys())[i]

            row=[str(mykey)]                              # Trajectories
#            print(mykey,data[mykey],'MY KEY ,DATA ')

            row.append(data[mykey][-1])                   # Times Seen
            maxTMPreached=max(np.transpose(data[mykey][0])[1])
            max
            row.append(maxTMPreached)                     # max TMP reached
            if maxTMPreached==maxTMP:
                row.append(1)                             # Are we reached the maximum TMP conc?
            else:
                row.append(0)
            row.append(mykey[-1])                         # Which genotype were we when we died?
            row.append(str(data[mykey][0]))               # Path 
            cur.execute(cmd2,row)
    end=time.time()
    print ('DB Exporting Time: ', end-start)
    return True



def simulation(mutant,drug,trajectory,path,mutations):

    if drug<maxTMP:
        drugnow=findmic(mutant,fitthr)

        if drugnow>maxTMP:
            path.append((mutant,maxTMP))
            return(trajectory,path,mutations)
        else:
            path.append((mutant,drugnow))
            randnum=randint(0,graphrowlen)
            newmutant=int(graph[mutant][randnum])
            newdrug=findmic(newmutant,fitthr)
            mutations.append(graphcols[randnum])
            trajectory.append(newmutant)

            if newdrug<drugnow or randnum==blockme:  # change statement after the or to block other mutations. Now PROMOTER is blocked.
                if randnum==6:
                    path.append((newmutant,drugnow))
                else:
                    path.append((newmutant,max([newdrug,0])))
                return(trajectory,path,mutations)
            else:
                path.append((newmutant,drugnow))
                simulation(newmutant,newdrug,trajectory,path,mutations)
    else:
        path.append((mutant,maxTMP))
        return(trajectory,path,mutations)

    return(trajectory,path,mutations)

fitpcts=[.5]#[.5,.1,.01,.001]#
#for fitpct in fitpcts:
#    fitthr=fitpct
#    graphrowlen=rowlen[1]
#    a=simulation(0,0,[0],[(0,0)],[])
timenow=str(dtdt.now()).replace('-','_').replace(' ','_').replace(':','_').replace('.','_')[0:19]
for timesrun in [1000000]:
    print ('Simulation is gonna run ',timesrun,' times')
    for fitpct in fitpcts:
        fitthr=fitpct
        print ('Fitness is x% of WT & x: ', fitpct*100.0)
        wtext=['NP-','WP-']
        for simmode in simmodes:
            graphrowlen=rowlen[simmode]
            sparallel=time.time()
            # what are your inputs, and what operation do you want to
            # perform on each input. For example...
            

            num_cores = cpu_count()
            results = Parallel(n_jobs=num_cores)(delayed(simulation)(startwith,0,[startwith],[(startwith,0)],[]) for inp in range(timesrun))
            eparallel=time.time()
            
            print ('Parallel Processing Time: ',eparallel-sparallel)
            name='SW0_FT'+str(fitpct*100)+'_'+wtext[simmode]+'Times_'+str(timesrun)+'_'+timenow
            filename=name+'.pickle'

            trajectories=pack_results(results)
            zipickle(trajectories,zipicklefolder,filename)
            export_db(trajectories,zipicklefolder,filename)
#            print(trajectories)