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

# sns.displot(random.uniform(size=1000), kind="kde")
# x = random.multinomial(n=6, pvals=[1/6, 1/6, 1/6, 1/6, 1/6, 1/6])
# sns.displot(random.exponential(size=1000), kind="kde")

# sns.displot(random.chisquare(df=1, size=1000), kind="kde")


# sns.displot(random.pareto(a=2, size=1000))


x = random.zipf(a=2, size=1000)
sns.displot(x[x<10])


# plt.show()


x = [1, 2, 3, 4]
y = [4, 5, 6, 7]
z = np.add(x, y)


# print(z)


def myadd(x, y):
  return x+y


myadd = np.frompyfunc(myadd, 2, 1)

# print(myadd([1, 2, 3, 4], [5, 6, 7, 8]))


ar1 = np.array([10, 11, 12, 13, 14, 15])
ar2 = np.array([20, 21, 22, 23, 24, 25])

newar = np.add(ar1, ar2)
newar2 = np.subtract(ar1, ar2)

print(newar2)

