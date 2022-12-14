import os
import sys
import sympy as sp

casepath = r'/Users/zeemarquez/openfoam/assignment/freestream/grid2/case'

def prepareBoundary(casepath):
    boundarypath = casepath + r'/constant/polyMesh/boundary'
    f = open(boundarypath,'r')
    text = f.read()
    f.close()
    text = text.replace('\n        physicalType    patch;','')
    boundary = None
    newLines = []
    for i,line in enumerate(text.split('\n')):
        newline = line
        if 'type ' in line and 'patch' in line:
            boundary = ''.join(text.split('\n')[i-2].split())
            if boundary == 'Side':
                newline = line.replace('patch','empty')
            elif boundary == 'Floor':
                newline = line.replace('patch','wall')
            elif boundary == 'Airfoil':
                newline = line.replace('patch','wall')
            
        
        newLines.append(newline)

    newtext = '\n'.join(newLines)
    o = open(boundarypath,'w')
    o.write(newtext)

def getApplication(casepath):

    controlpath = casepath + r'/system/controlDict'

    f = open(controlpath,'r')
    text = f.read()
    f.close()

    for line in text.split('\n'):
        sline = line.split()
        if len(sline) > 0:
            if sline[0] == 'application':
                return sline[1].replace(';','')
     
def solveforyplus(N,L,yw):
    x = sp.symbols('x')
    eq = sp.Eq((L*(x-1))/(x**(N-1)-1) - yw,0)
    sol = sp.nsolve(eq,0)
    return float(str(sol))
    
         
    

try:
    arg = sys.argv[1]
except:
    raise Exception("One argument expected, got none")

if len(sys.argv) > 2:
    casepath = sys.argv[2]
else:
    casepath = os.getcwd()

if arg == 'application':
    try:
        print(getApplication(casepath))
    except:
        print('error')
elif arg == 'boundary':
    try:
        prepareBoundary(casepath)
    except:
        print('error')
    
else:
    raise Exception("Invalid argument passed")
    

#%%
import matplotlib.pyplot as plt

logpath = r'/Users/zeemarquez/openfoam/assignment/groundeffect/case/log.csv'

logdic = {}
f = open(logpath,'r')
text = f.read()
f.close()
lines= text.split('\n')
headers = lines[0].split(';')

for header in headers:
    logdic[header] = []

for line in lines[1:]:
    cols = line.split(';')
    
    for col, key in zip(cols,logdic.keys()):
        logdic[key].append(col)

logdic['T'] = logdic['T'][:-1]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

    
ax.clear()
for key in logdic.keys():
    if key != 'T':
        ax.plot(logdic['T'],logdic[key], label = key)

plt.yscale('log')
plt.grid(which='both')
plt.title('Residuals')
plt.legend(loc='upper right')
fig.set_size_inches(10, 6)
fig.tight_layout()
plt.show()
# %%
def sieve(n):
    x = [1]*n
    x[1] = 0
    for i in range(2, int(n/2)):
        j = 2*i
        while j < n:
            x[j] = 0
            j = j + i
    return x

def prime(n,x):
    i,j = 1,1
    while j <= n:
        if x[i] == 1:
            j+=1
        i+=1
    return i - 1

x = sieve(10000)
code = [1206, 301, 384, 5]
key = [1,1,2,2]

p = ''
for i in range(0,4):
    p+=str(prime(code[i],x)- key[i])

print(p)
# %%
