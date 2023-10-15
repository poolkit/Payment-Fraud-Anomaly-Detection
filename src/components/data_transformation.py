import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

def GetXy(train, test):
    X_train = train.drop('Label', axis=1)
    y_train = train['Label']
    X_test = test.drop('Label', axis=1)
    y_test = test['Label']
    return X_train, y_train, X_test, y_test

class TimestampTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns
    
    def fit(self, X, y=None):
        if not isinstance(X, pd.DataFrame):
            raise ValueError(f"{X} must be a pandas DataFrame")
        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            raise ValueError(f"{X} must be a pandas DataFrame")
        
        if self.columns is None:
            return X
        else:
            X_ = X.copy()
            for each in self.columns:
                X_[each] = pd.to_datetime(X[each])
                day = X_[each].dt.day
                hour = X_[each].dt.hour
                day_of_week = X_[each].dt.dayofweek
                X_['DaySin'] = np.sin(2 * np.pi * day / 31)
                X_['DayCos'] = np.cos(2 * np.pi * day / 31)
                X_['HourSin'] = np.sin(2 * np.pi * hour / 24)
                X_['HourCos'] = np.cos(2 * np.pi * hour / 24)
                X_['DoWSin'] = np.sin(2 * np.pi * day_of_week / 7)
                X_['DoWCos'] = np.cos(2 * np.pi * day_of_week / 7)
            return X_

class InteractionTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.grouping_columns = ['Sender_Id', 'Bene_Id']

    def fit(self, X, y=None):
        if not isinstance(X, pd.DataFrame):
            raise ValueError(f"{X} must be a pandas DataFrame")

        self.interaction_frequency = X.groupby(self.grouping_columns).size().reset_index().rename(columns={0: 'Interaction_Frequency'})
        self.interaction_amount = X.groupby(self.grouping_columns)['USD_amount'].mean().reset_index().rename(columns = {'USD_amount':'Amount_Mean'})
        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            raise ValueError(f"{X} must be a pandas DataFrame")
            
        X_ = X.copy()
        X_ = pd.merge(X_, self.interaction_frequency, on=self.grouping_columns, how='left')
        X_['Interaction_Frequency'] = X_['Interaction_Frequency'].fillna(0)
        X_ = pd.merge(X_, self.interaction_amount, on=self.grouping_columns, how='left')
        X_['Amount_Mean'] = X_['Amount_Mean'].fillna(X_['Amount_Mean'].mean())
        return X_

class CubeRootTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns
    
    def fit(self, X, y=None):
        if not isinstance(X, pd.DataFrame):
            raise ValueError(f"{X} must be a pandas DataFrame")
        return self
    
    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            raise ValueError(f"{X} must be a pandas DataFrame")
            
        if self.columns is None:
            return X
        else:
            X_ = X.copy()
            X_[self.columns] = X_[self.columns].apply(lambda x: np.cbrt(x))
            return X_

class TargetEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
        self.mapping = {}
        self.target = 'Label'
    
    def fit(self, X, y):
        if not isinstance(X, pd.DataFrame):
            raise ValueError(f"{X} must be a pandas DataFrame")
        
        y.name = self.target
        X_ = pd.concat([X,y], axis=1)
        for col in self.columns:
            encoding_map = X_.groupby(col)[self.target].mean().to_dict()
            self.mapping[col] = encoding_map
        return self
        
    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            raise ValueError(f"{X} must be a pandas DataFrame")

        X_ = X.copy()
        for col in self.columns:
            X_[col] = X_[col].map(self.mapping[col])
            X_[col] = X_[col].fillna(np.array(list(self.mapping[col].values())).mean())
        return X_

class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self, dropping_columns):
        self.dropping_columns = dropping_columns
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_ = X.copy()
        return X_.drop(self.dropping_columns, axis=1)
