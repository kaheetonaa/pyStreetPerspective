import numpy as np
import matplotlib.pyplot as plt

prediction=np.load('prediction.npz')

depth = prediction['depth'][0][0]
c=depth.shape[0]

profile=[float(i[0]) for i in depth[int(c/2),:]]

plt.plot(profile)
plt.show()
