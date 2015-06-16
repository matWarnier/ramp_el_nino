from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator
from sklearn.decomposition import KernelPCA

class Regressor(BaseEstimator):
    def __init__(self):
        self.clf = Pipeline([('scaler', StandardScaler()),
                             # ('KernelPCA',KernelPCA(n_components=10)),
                             ("RF", RandomForestRegressor(n_estimators=100, max_depth=15))])

    def fit(self, X, y):
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)
