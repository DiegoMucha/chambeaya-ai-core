from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

# Script para el modelo de IA - KawsAI

# Primero creamos la clase para nuestro modelo de IA
class KawsAIModel:
    # Se usa el modelo de knn y se inicializa con 2 principales parametros
    # n_neighbors = El número de mejores match que se va a mostrar
    # metric = El tio de métrica y comparación que se va a usar 
    def __init__(self):
        self.knn = NearestNeighbors(n_neighbors=3, metric='euclidean')
    # Para el entrenamiento se va a usar las matrices TF-IDF de los puestos como parametro y se usará el metodo fit
    def train(self, X_puestos):
        self.knn.fit(X_puestos)
    # Función para obtener los mejores matches, se retornará los índices.
    def get_positions(self, X_estudiante_nuevo):
        distances, indexes = self.knn.kneighbors(X_estudiante_nuevo)
        return distances[0], indexes[0]