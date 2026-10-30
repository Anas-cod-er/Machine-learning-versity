import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# sns.displot([0, 1, 2, 3, 4, 5])
sns.displot([0, 1, 2, 3, 4, 5], kind="kde")
x = np.random.normal(loc=1, scale=2, size=(2, 3))


plt.show()

print(x)