from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator
from sklearn.decomposition import KernelPCA

class Regressor(BaseEstimator):
    def __init__(self):
        self.clf = Pipeline([('scaler', StandardScaler()),
                             #('KernelPCA',KernelPCA(n_components=10)),
                             ("GBR", GradientBoostingRegressor(n_estimators=500))])

    def fit(self, X, y):
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)
