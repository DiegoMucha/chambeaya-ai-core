# from fastapi import FastAPI
# from api_service.match_job_student.ep_mjs import model
# import pandas as pd
# from preprocessing.preprocesador import Preprocesador
# from fastapi import Body

# app = FastAPI()
# preprocesador = Preprocesador()

# @app.get("/")
# def root():
#     return {"message": "Servidor de prueba para IA (sin backend)"}

# @app.post("/test_match/")
# def test_match(estudiante: dict = Body(...)):
#     df_puestos = pd.read_csv("datasets/puestos_test.csv")
#     df_estudiante = pd.DataFrame([estudiante])

#     X_puestos = preprocesador.fit_transform(df_puestos)
#     X_estudiante = preprocesador.transform_estudiante(df_estudiante)
    
#     n_ofertas = len(df_puestos)
#     n_neighbors = min(3, n_ofertas)
    
#     model.knn = model.knn.__class__(n_neighbors=n_neighbors, metric='cosine')
#     model.train(X_puestos)
#     indexes = model.get_positions(X_estudiante)
#     return {
#         "indexes": indexes.tolist(),
#         "puestos_ids": df_puestos.iloc[indexes.tolist()].to_dict(orient="records")
#     }