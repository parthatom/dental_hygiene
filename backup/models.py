import numpy as np
import pandas as pd
import matplotlib as plt
from preprocess_dental import preprocess_dental_data
from data_preprocess import preprocess
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier


def pre_processing(label='SERIOUS_01'):
    '''
    Split Data into train-test after scaling, PCA and One hot encodings
    @param label: Y Label
    @return: Processed Data
    '''
    labels = ['SERIOUS_01']

    # Get Data
    data = preprocess(for_modelling=True)
    dental_data = preprocess_dental_data(usage='01', drop_all_na=True, skipna=False, set_index=True)[labels]
    data = pd.merge(dental_data, data, left_index=True, right_index=True)

    # Numerical and Categorical Data
    Y = data[labels]
    data = data.drop(columns=labels)
    categorical_cols = list(filter(lambda x: isinstance(data[x].dtype, pd.api.types.CategoricalDtype), data.columns))
    numerical_cols = list(filter(lambda x: x not in categorical_cols, data.columns))
    num_data = data[numerical_cols]

    # Scale and PCA
    scaler = StandardScaler().fit_transform(num_data)
    pca = PCA(n_components=3).fit_transform(scaler)

    # One Hot Encoding
    cat_data = data[categorical_cols]
    ohe = OneHotEncoder(sparse=False).fit_transform(cat_data)

    data = pd.concat([Y.reset_index(drop=True), pd.DataFrame(pca), pd.DataFrame(ohe)], axis=1)

    y = data[label]
    x = data.drop(columns=labels)
    X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2)
    return X_train, X_test, Y_train, Y_test


def get_score(clf, X_train, X_test, Y_train, Y_test):
    '''
    Train and get accuracy of cld
    @param clf: Classifier
    @param X_train: Train X
    @param X_test: Test X
    @param Y_train: Train Y
    @param Y_test: Test Y
    @return: accuracy
    '''
    clf.fit(X_train, Y_train)
    return clf.score(X_test, Y_test)


def train(label=None):
    '''
    Train the various models
    @param labels: Simple 01 or Serious 01, Defaults to Serious 01
    @return: Dict {model:accuracy}
    '''
    X_train, X_test, Y_train, Y_test = pre_processing()
    names = ['Random Forest', 'SVM_RBC', 'SVM_Poly', 'QDA']
    clfs = [RandomForestClassifier(max_depth=2, random_state=0),
            SVC(),
            SVC(kernel='poly'),
            QuadraticDiscriminantAnalysis(),
            ]
    scores = [get_score(clf, X_train, X_test, Y_train, Y_test) for clf in clfs]
    names.append('ADABoost')
    scores.append(get_score(AdaBoostClassifier(base_estimator=clfs[0]), X_train, X_test, Y_train, Y_test))
    d = {}
    for n,s in zip(names,scores):
        d[n] = s
    return d


if __name__ == '__main__':
    print(train())
