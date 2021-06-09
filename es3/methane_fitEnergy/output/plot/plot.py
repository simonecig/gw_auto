import matplotlib.pyplot as plt
import pandas as pd

data8 = pd.read_csv("./8_re4", sep=' ', index_col=False, names=['1','2','3','4'])
plt.plot(data8['1'], data8['2'])
print(data8)
plt.show()
