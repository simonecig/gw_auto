import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# read data from file
data = pd.read_csv("./data.txt", sep='\t', index_col=False)

# plot data
fig, ax = plt.subplots(2,2)
ax[0][0].plot(data.cutoff, data.tot_energy, 'p--', color='royalblue' )
ax[0][1].plot(data.cutoff, data.HOMO, 'p--', color='royalblue' )
ax[1][0].plot(data.cutoff, data.LUMO, 'p--', color='royalblue' )
ax[1][1].plot(data.cutoff, data.time_wall, 'p--', color='royalblue' )

# plot titles 
ax[0][0].set_title('cutoff vs en_tot')
ax[0][1].set_title('cutoff vs HOMO')
ax[1][0].set_title('cutoff vs LUMO')
ax[1][1].set_title('cutoff vs time (wall)')

# x labels
ax[0][0].set_xlabel('cutoff (Ry)')
ax[0][1].set_xlabel('cutoff (Ry)')
ax[1][0].set_xlabel('cutoff (Ry)')
ax[1][1].set_xlabel('cutoff (Ry)')

# y labels
ax[0][0].set_ylabel('total energy (Ry)')
ax[0][1].set_ylabel('HOMO (eV)')
ax[1][0].set_ylabel('LUMO (eV)')
ax[1][1].set_ylabel('wall time (s)')


fig.tight_layout()
plt.show()
