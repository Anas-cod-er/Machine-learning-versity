from sklearn.linear_model import LinearRegression
import numpy as np

# Training data: hours studied
X = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)

# Exam scores
y = np.array([35, 40, 50, 55, 65, 75])

# Create and train the model
model = LinearRegression()
model.fit(X, y)

# Predict a score for 7 hours of study
prediction = model.predict([[7]])

print("Predicted score:", prediction[0])