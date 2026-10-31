import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from numpy import random

# sns.displot([0, 1, 2, 3, 4, 5])
# sns.displot([0, 1, 2, 3, 4, 5], kind="kde")
# x = np.random.normal(loc=1, scale=2, size=(2, 3))

# sns.displot(random.binomial(n=10, p=0.5, size=1000))

data = {
  "normal": random.normal(loc=50, scale=5, size=1000),
  "binomial": random.binomial(n=100, p=0.5, size=1000)
}

# sns.displot(data, kind="kde")

sns.displot(random.uniform(size=1000), kind="kde")


plt.show()

# print(x)