import numpy as np
import pandas as pd
from sklearn.model_selection import (
    train_test_split, StratifiedKFold, cross_val_score
)
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score
)

rng = np.random.default_rng(2026)
n = 500
outlook = rng.choice(
    ['Sunny', 'Overcast', 'Rainy'], n,
    p=[0.40, 0.25, 0.35]
)
temp = rng.integers(14, 39, n).astype(float)
humidity = rng.integers(35, 96, n).astype(float)
wind = rng.integers(2, 43, n).astype(float)



risk = (
    (outlook == 'Rainy') * 2.0
    + (wind > 29) * 1.5
    + (humidity > 78) * 0.8
    + ((temp < 18) | (temp > 34)) * 1.0
    - (outlook == 'Overcast') * 0.45
)
risk = risk + rng.normal(0, 0.5, n)
play = np.where(risk < 2.3, 'Yes', 'No')

df2 = pd.DataFrame({
    'Outlook': outlook,
    'TemperatureC': temp,
    'HumidityPct': humidity,
    'WindKmh': wind,
    'Play': play
})
df2.insert(0, 'ID', range(1, n + 1))


for col, count in [
    ('Outlook', 5), ('TemperatureC', 8), ('HumidityPct', 6)
]:
    ix = rng.choice(n, size=count, replace=False)
    df2.loc[ix, col] = np.nan

print("--- F4: Dataset Inspection ---")
print(df2.head(6).to_string(index=False))
print('Shape:', df2.shape)
print('Labels:\n', df2['Play'].value_counts())
print('Missing:\n', df2.isna().sum())



df2.to_csv('golf_weather_300.csv', index=False)
loaded = pd.read_csv('golf_weather_300.csv')
print('\nReloaded shape:', loaded.shape)
df2 = loaded




X2 = df2.drop(columns=['ID', 'Play'])
y2 = df2['Play']
print('Feature names:', X2.columns.tolist())



X2_train, X2_test, y2_train, y2_test = train_test_split(
    X2, y2, test_size=0.30,
    stratify=y2, random_state=42
)
print('Train/Test sizes:', len(X2_train), len(X2_test))




cat_cols = ['Outlook']
num_cols = ['TemperatureC', 'HumidityPct', 'WindKmh']

prep2 = ColumnTransformer([
    ('cat', Pipeline([
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ]), cat_cols),
    ('num', SimpleImputer(strategy='median'), num_cols)
])

def large_tree(depth):
    return Pipeline([
        ('prep', prep2),
        ('dt', DecisionTreeClassifier(
            max_depth=depth, random_state=42
        ))
    ])




cv2 = StratifiedKFold(
    n_splits=5, shuffle=True, random_state=42
)
for i, (train_idx, val_idx) in enumerate(
    cv2.split(X2_train, y2_train), 1
):
    print('Fold', i, 'train', len(train_idx),
          'validation', len(val_idx))




all_scores = {}
for depth in [2, 4, 6, None]:
    scores = cross_val_score(
        large_tree(depth), X2_train, y2_train,
        cv=cv2, scoring='accuracy'
    )
    all_scores[depth] = scores
    print(depth, scores.round(4), round(scores.mean(), 4))





best_depth = sorted(
    all_scores,
    key=lambda d: (-all_scores[d].mean(), 10000 if d is None else d)
)[0]
print('Selected depth:', best_depth)



final_model = large_tree(best_depth)
final_model.fit(X2_train, y2_train)
y2_pred = final_model.predict(X2_test)
print('\nPredictions:', len(y2_pred))




cm2 = confusion_matrix(
    y2_test, y2_pred, labels=['Yes', 'No']
)
print('Confusion Matrix:\n', cm2)




print('\n--- H4: Final Test Metrics ---')
print('Accuracy:', round(accuracy_score(y2_test, y2_pred), 4))
print('Precision:', round(precision_score(y2_test, y2_pred, pos_label='Yes'), 4))
print('Recall:', round(recall_score(y2_test, y2_pred, pos_label='Yes'), 4))
print('F1:', round(f1_score(y2_test, y2_pred, pos_label='Yes'), 4))
                                     