import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib

data = pd.read_csv("muse_app/datas/data.csv")

song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=10))])
X = data.select_dtypes(np.number)
number_cols = list(X.columns)
song_cluster_pipeline.fit(X)

def get_pipeline() :
    joblib.dump(song_cluster_pipeline, 'pipe.joblib')
    pipe = joblib.load('pipe.joblib')
    return pipe

def get_data() :
    pipe = get_pipeline()
    song_cluster_labels = pipe.predict(X)
    data['cluster_label'] = song_cluster_labels
    
    return data