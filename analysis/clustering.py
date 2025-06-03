from sklearn.cluster import KMeans
import numpy as np

def cluster_prey_traits(prey_list, n_clusters: int):
    X = []
    for p in prey_list:
        X.append([p.traits["speed"], p.traits["agility"], p.traits["vision"]])
    X = np.array(X)

    if len(X) < n_clusters:
        return None, None

    kmeans = KMeans(n_clusters=n_clusters, n_init="auto")
    labels = kmeans.fit_predict(X)
    centroids = kmeans.cluster_centers_
    return labels, centroids
