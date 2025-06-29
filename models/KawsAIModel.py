from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

# Script para el modelo de IA - KawsAI

# Primero creamos la clase para nuestro modelo de IA
class KawsAIModel:
    # Se usa el modelo de knn y se inicializa con 2 principales parametros
    # n_neighbors = El número de mejores match que se va a mostrar
    # metric = El tio de métrica y comparación que se va a usar 
    def __init__(self):
        self.knn_offer = NearestNeighbors(n_neighbors=3, metric='cosine')
        self.knn_student = NearestNeighbors(n_neighbors=3, metric='cosine')
    def get_best_offers(self, embedding_offers, embedding_student):
        self.knn_student.fit(embedding_offers)
        distances, indexes = self.knn_student.kneighbors(embedding_student)
        return 1 - distances[0], indexes[0]
    def get_best_students(self, embeddings_students, embedding_offer):
        self.knn_offer.fit(embeddings_students)
        distances, indexes = self.knn_offer.kneighbors(embedding_offer)
        return 1 - distances[0], indexes[0]