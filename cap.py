import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


with open('127.0.0.1.json', 'r') as file: # prepare for numpy
    raw_data = file.read()
    fixed_data = f"[{raw_data.replace('}{', '},{')}]"
    data = json.loads(fixed_data)

values = [list(map(float, item["MSG"][0].split(','))) for item in data]
values = np.array(values)

time = values[:, 0] / 1440.0
weather = values[:, 1]
temperature = values[:, 2]

scaler = StandardScaler()
scaled_values = scaler.fit_transform(values)

pca = PCA(n_components=2)
reduced_values = pca.fit_transform(scaled_values)

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(reduced_values)
    wcss.append(kmeans.inertia_)

sil_scores = []
for i in range(2, 11):  # score is not defined for 1 cluster
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(reduced_values)
    score = silhouette_score(reduced_values, kmeans.labels_)
    sil_scores.append(score)


delta_wcss = np.diff(wcss)
elbow_point = np.argmin(delta_wcss) + 1 
optimal_clusters_silhouette = np.argmax(sil_scores) + 2

optimal_clusters = max(elbow_point, optimal_clusters_silhouette)

print(f"Optimal number of clusters (based on elbow and silhouette score): {optimal_clusters}")

# k-means++ clustering
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=42)
kmeans.fit(reduced_values)

labels = kmeans.labels_
centers = kmeans.cluster_centers_

ranges = []
for cluster in range(optimal_clusters):
    cluster_data = values[labels == cluster]
    time_range = (np.min(cluster_data[:, 0]), np.max(cluster_data[:, 0]))
    weather_range = (np.min(cluster_data[:, 1]), np.max(cluster_data[:, 1]))
    temperature_range = (np.min(cluster_data[:, 2]), np.max(cluster_data[:, 2]))
    
    if time_range[1] < time_range[0]:  # if the range crosses midnight
        time_range = ((0, time_range[1]), (time_range[0], 1440))
    
    ranges.append({
        'cluster': cluster,
        'time_range': time_range,
        'weather_range': weather_range,
        'temperature_range': temperature_range
    })

for r in ranges:
    print(f"Cluster {r['cluster']}:")
    print(f"  Time Range: {r['time_range']}")
    print(f"  Weather Range: {r['weather_range']}")
    print(f"  Temperature Range: {r['temperature_range']}\n")
