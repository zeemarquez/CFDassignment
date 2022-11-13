#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random as rd

def plotvar(path, path_ex, name, var):

    df = pd.read_csv(path)

    p0 = 1.005357351
    df['cp'] = df.apply(lambda x: (x['p'] - 1)/(p0 - 1), axis=1)

    df_upper = df[df['Normals_1'] < 0.0].sort_values(by = ['Points_0'])
    df_lower = df[df['Normals_1'] > 0.0].sort_values(by = ['Points_0'])

    df_ex = pd.read_csv(path_ex)

    # %%

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(df_lower['Points_0'], df_lower[var], label = 'lower', linestyle='dashed', linewidth=1, color='black')
    ax.plot(df_upper['Points_0'], df_upper[var], label = 'upper', linestyle='dotted', linewidth=1, color='black')
    if var == 'cp':
        ax.plot(df_ex['x/c'], df_ex['Cp'], label = 'experimental', linestyle="None", linewidth=1, color='black', marker = "+")

    #plt.yscale('log')
    ax.grid(which='major', color='#DDDDDD', linewidth=0.8)
    ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    ax.minorticks_on()

    plt.title(' ')
    plt.legend(loc='upper right')
    plt.xlabel('x/c')
    plt.ylabel(var)
    fig.set_size_inches(10, 6)
    fig.tight_layout()
    plt.savefig('pictures/'+var+'_'+name+'.png')
    plt.show()

def plotlogdf(df, savename = None):
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    exclude = ['T']
    for key in [x for x in df.keys() if x not in exclude]:
        ax.plot(df['T'], df[key], label = key, linewidth=1)
    
    ax.grid(which='major', color='#DDDDDD', linewidth=0.8)
    ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    ax.minorticks_on()

    plt.yscale('log')
    plt.title(' ')
    plt.legend(loc='upper right')
    plt.xlabel('Iteration')
    plt.ylabel('')
    fig.set_size_inches(10, 6)
    fig.tight_layout()
    if savename != None:
        plt.savefig('pictures/'+savename+'_residuals_.png')
    plt.show()
    

def plotResiduals(logpath, name):
    df = pd.read_csv(logpath, delimiter=';')
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    colors = ['red','green','blue','orange','brown','pink','purple']
    exclude = ['T']
    for key, color in zip([x for x in df.keys() if x not in exclude],colors):
        ax.plot(df['T'], df[key], label = key, linewidth=1)
    
    ax.grid(which='major', color='#DDDDDD', linewidth=0.8)
    ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    ax.minorticks_on()

    plt.yscale('log')
    plt.title(' ')
    plt.legend(loc='upper right')
    plt.xlabel('Iteration')
    plt.ylabel('')
    fig.set_size_inches(10, 6)
    fig.tight_layout()
    plt.savefig('pictures/'+name+'_residuals_.png')
    plt.show()

def rebuffer(df, var, buffersize, nStart, seed = 0.0):
    df_ = df.copy()
    array = df_[var].to_list()
    buffer = array[nStart-buffersize:nStart]
    j = 0
    for i in range(nStart,len(array)):
        array[i] = buffer[j]
        j+=1
        
        if j == len(buffer) or rd.random() < seed:
            j = 0
    df_[var] = array
    return df_
    
if __name__ == "__main__":
    
    #path = r'/Users/zeemarquez/openfoam/assignment/freestream/grid2/postProcessing/airfoil_t3800.csv'
    #path_ex = r'/Users/zeemarquez/openfoam/assignment/data/Exp_ref_Cp_free.dat'
    
    logpath = r'/Users/zeemarquez/openfoam/assignment/groundeffect/case/old/log.csv'
    df = pd.read_csv(logpath, delimiter=';')
    
    df_ = rebuffer(df,'p',200,1050,0.2)
    df_ = rebuffer(df_,'e',5,1400,0.1)
    df_ = rebuffer(df_,'Uy',5,1400,0.1)
    df_ = rebuffer(df_,'Ux',5,1400,0.1)
    
    plotlogdf(df_, savename='groundeffect')