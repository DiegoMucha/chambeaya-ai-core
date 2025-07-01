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
    def get_best_job_offers(self, job_offer_embeddings, student_embedding):
        # student_embedding debe ser generado usando los campos: name, email, career, description, weekly_availability, preferred_modality, experience_id, date_of_birth, skills, interests
        self.knn_student.fit(job_offer_embeddings)
        distances, indexes = self.knn_student.kneighbors(student_embedding)
        return 1 - distances[0], indexes[0]
    def get_best_students(self, student_embeddings, job_offer_embedding):
        # job_offer_embedding debe ser generado usando los campos de la clase correspondiente a la oferta en inglés
        self.knn_offer.fit(student_embeddings)
        distances, indexes = self.knn_offer.kneighbors(job_offer_embedding)
        return 1 - distances[0], indexes[0]