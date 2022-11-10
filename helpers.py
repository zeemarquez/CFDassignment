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