from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

class KawsAIModel:
    def __init__(self):
        self.knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    def train(self, X_puestos):
        self.knn.fit(X_puestos)
    def get_positions(self, X_estudiante_nuevo):
        distances, indexes = self.knn.kneighbors(X_estudiante_nuevo)
        return distances[0], indexes[0]