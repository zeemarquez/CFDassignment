#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

path = r'/Users/zeemarquez/openfoam/assignment/freestream/grid2/postProcessing/airfoil_t3800.csv'
path_ex = r'/Users/zeemarquez/openfoam/assignment/data/Exp_ref_Cp_free.dat'

df = pd.read_csv(path)

p0 = 1.005357351
df['cp'] = df.apply(lambda x: (x['p'] - 1)/(p0 - 1), axis=1)

df_upper = df[df['Normals_1'] < 0.0].sort_values(by = ['Points_0'])
df_lower = df[df['Normals_1'] > 0.0].sort_values(by = ['Points_0'])

df_ex = pd.read_csv(path_ex)

# %%

name = 'freestream_grid2'
var = 'yPlus'

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

