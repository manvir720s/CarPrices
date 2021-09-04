import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import math

#use mileage, engine, maxpower to determine price

dataset = pd.read_csv('Car details v4.csv', nrows=800)
dataset = dataset.drop(dataset.columns[0], axis = 1)

#remove units 
# (mileage = kmpl, km/kg), (engine = CC), (maxpower = bhp)\
str_factors = ["mileage", "engine", "max_power"]

for i in range(0, len(str_factors)):
    test_list = dataset[str_factors[i]]
    print(str_factors[i])
    #remove units
    if(str_factors[i] == "mileage"):
        test_list = dataset["mileage"].str.strip('kmpl')
        test_list = test_list.str.strip('km/kg')
    elif (str_factors[i] == "engine"):
        test_list = dataset["engine"].str.strip('CC')
    else:
        test_list = dataset["max_power"].str.strip('bhp')
    #convert to float
    for j in range(0, len(test_list)):
        test_list[j] = float(test_list[j])
    '''
    print(str_factors[i])
    print(test_list.mean())
    print(test_list.isnull().sum())
    print(end='\n')
    '''
    test_list.fillna(test_list.mean(), inplace = True)
    dataset[str_factors[i]] = test_list
    
X = pd.DataFrame(dataset.iloc[:,[2, 7, 8,9]])
y = pd.DataFrame(dataset.iloc[:,1])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/10, random_state = 2)

from sklearn.linear_model import LinearRegression
regressor = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=True)
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)


#r_sq = regressor.fit(X_train, y_train).score(X_test, y_test) # closer to one is better 
#print('coefficient of determination: ', r_sq)

def classify(a, b, c, d):
    arr = np.array([a, b, c, d]) # Convert to numpy array
    arr = arr.astype(np.float64) # Change the data type to float
    query = arr.reshape(1, -1) # Reshape the array
    prediction = regressor.predict(query)[0] 
    rounded_prediction = np.round(prediction, 2)
    return rounded_prediction # Return the prediction

