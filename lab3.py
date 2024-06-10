# -*- coding: utf-8 -*-
"""lab3

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cjYfYifxaA8kikexDV3uoQwoiD47LO5Z
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

TESTDATA = "./sample_data/TestData_new.csv"
TRAINDATA = "./sample_data/TrainData_new.csv"
dtest = pd.read_csv(TESTDATA)
dtrain = pd.read_csv(TRAINDATA)

dtrain.head()

"""пропуски есть и в тестовых и тренировочных данных, в тренировочной выборке пропуски есть в 13 столбцах"""

dtest.isnull().sum()

missing = dtrain.isnull().sum()
print(missing)

"""заполнение пропусков. с наибольшим кол-вом пропусков "feature_4"
"""

max_isnull = missing.idxmax()

mean = dtrain[max_isnull].mean()
print(mean)

"""В столбце с наибольшим количеством пропусков заполните пропуски средним значением по столбцу. среднее = 70.63761049589014"""

dtrain[max_isnull].fillna(mean, inplace=True)

"""с наименьшим кол-вом пропусков "feature_6", всего строк 69"""

min_isnull = missing[missing > 0].idxmin()
print(min_isnull)

len(dtrain[dtrain[min_isnull].isnull()])

dtrain.dropna( subset = [min_isnull], inplace = True)

"""столбцы в таблице (не считая target) содержат меньше 5 различных значений - 2"""

unique = dtrain.drop(columns=['target']).nunique()
print(unique)

unique[unique < 5].count()

"""Вычислите долю ушедших из компании клиентов, для которых значение признака 2 больше среднего значения по столбцу, а значение признака 13 меньше медианы по столбцу."""

feature2_mean = dtrain['feature_2'].mean()
feature13_median = dtrain['feature_13'].median()

clients_leave = dtrain[(dtrain['feature_2'] > feature2_mean) & (dtrain['feature_13'] < feature13_median)]

len(clients_leave[clients_leave['target'] == 1])/len(clients_leave)

"""Разбейте тренировочные данные на целевой вектор y, содержащий значения из столбца target, и матрицу объект-признак X, содержащую остальные признаки. Обучите на этих данных логистическую регрессию из sklearn (LogisticRegression) с параметрами по умолчанию. Выведите среднее значение метрики f1-score алгоритма на кросс-валидации с тремя фолдами. Ответ округлите до сотых.
При объявлении модели фиксируйте random_state = 42.

"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score, make_scorer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction import DictVectorizer

y = dtrain['target']
X = dtrain.drop(columns=['target'])

X = pd.get_dummies(X, columns=['cat_feature_1', 'cat_feature_2'])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

for column in X.columns:
    if X[column].dtype == 'object':
        X[column].fillna(X[column].mode()[0], inplace=True)
    else:
        X[column].fillna(X[column].mean(), inplace=True)



model = LogisticRegression(random_state=42, solver='lbfgs', max_iter=10000)

f1_scorer = make_scorer(f1_score)
scores = cross_val_score(model, X, y, cv=3, scoring=f1_scorer)

mean_f1 = scores.mean()
print(mean_f1)

"""Подберите значение константы регуляризации C в логистической регрессии, перебирая гиперпараметр от 0.001 до 100 включительно, проходя по степеням 10. Для выбора C примените перебор по сетке по тренировочной выборке (GridSearchCV из библиотеки sklearn.model_selection) с тремя фолдами и метрикой качества - f1-score. Остальные параметры оставьте по умолчанию. В ответ запишите наилучшее среди искомых значение C."""

from sklearn.model_selection import GridSearchCV

param_grid = {'C': np.logspace(-3, 2, num=6)}

grid_search = GridSearchCV(model, param_grid, cv=3, scoring='f1')

grid_search.fit(X, y)

print("Наилучшее значение C:", grid_search.best_params_['C'])

"""Добавьте в тренировочные и тестовые данные новый признак 'NEW', равный произведению признаков '7' и '11'. На тренировочных данных с новым признаком заново с помощью GridSearchCV (с тремя фолдами и метрикой качества - f1-score) подберите оптимальное значение C (перебирайте те же значения C, что и в предыдущих заданиях), в ответ напишите наилучшее качество алгоритма (по метрике f1-score), ответ округлите до сотых."""

dtrain['NEW'] = dtrain['feature_7'] * dtrain['feature_11']

X = dtrain.drop(columns=['target'])
y = dtrain['target']

for column in X.columns:
    if X[column].dtype == 'object':
        X[column].fillna(X[column].mode()[0], inplace=True)
    else:
        X[column].fillna(X[column].mean(), inplace=True)

X = pd.get_dummies(X, columns=['cat_feature_1', 'cat_feature_2'])

model = LogisticRegression(random_state=42, solver='lbfgs', max_iter=5000)

param_grid = {'C': np.logspace(-3, 2, num=6)}

grid_search = GridSearchCV(model, param_grid, cv=3, scoring='f1')

grid_search.fit(X, y)

best_C = grid_search.best_params_['C']
best_f1_score = grid_search.best_score_

print("Наилучшее значение C:", best_C)
print("Наилучшее качество (f1-score)", (best_f1_score))

dtest.head()

dtest['NEW'] = dtest['feature_7'] * dtest['feature_11']

X_test = dtest.drop(columns=['target'])
y_test = dtest['target']

X_test = pd.get_dummies(X_test, columns=['cat_feature_1', 'cat_feature_2'])

for column in X_test.columns:
        X_test[column].fillna(X_test[column].median(), inplace=True)

best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
best_f1_score_test = f1_score(y_test, y_pred)

print(best_f1_score_test)