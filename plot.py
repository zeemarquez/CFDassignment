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
        if col  == '':
            val = 0
        else:
            val = float(col)
        logdic[key].append(val)

logdic['T'] = logdic['T'][:-1]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

N = 1500
    
ax.clear()
for key in logdic.keys():
    if key != 'T':
        ax.plot(logdic['T'][:N],logdic[key][:N], label = key)

plt.yscale('log')
plt.grid(which='both')
plt.title('Residuals')
plt.legend(loc='upper right')
fig.set_size_inches(10, 6)
fig.tight_layout()
plt.show()