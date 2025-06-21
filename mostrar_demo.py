from IPython.display import display
import ipywidgets as widgets
from models.KawsAIModel import KawsAIModel
from preprocessing.preprocesador import Preprocesador

def input_con_etiqueta(etiqueta, widget):
    return widgets.VBox([widgets.Label(value=etiqueta), widget])

estudiante_guardado = {}

    estudiante_guardado

    # Crear inputs
    nombre_completo = widgets.Text()
    correo = widgets.Text()
    carrera = widgets.Text()
    ciclo_actual = widgets.IntText()
    ubicacion = widgets.Text()
    areas_interes = widgets.Text()
    habilidades_destacadas = widgets.Text()
    motivacion_principal = widgets.Text()
    descripcion_personal = widgets.Textarea()
    horas_semanales = widgets.IntSlider(value=20, min=0, max=40, step=1)
    modalidad_de_trabajo = widgets.Dropdown(options=['Presencial', 'Híbrido', 'Remoto'], value='Remoto')
    experiencia_relevante = widgets.Textarea()
    link_portafolio_cv = widgets.Text()

    # Botón
    boton_enviar = widgets.Button(description="Guardar estudiante")

    # Función al presionar el botón
    def al_enviar(b):
        nonlocal estudiante_guardado  # Accede a la variable global
        estudiante_guardado = {
            "nombre_completo": nombre_completo.value,
            "correo": correo.value,
            "carrera": carrera.value,
            "ciclo_actual": ciclo_actual.value,
            "ubicacion": ubicacion.value,
            "areas_interes": areas_interes.value,
            "habilidades_destacadas": habilidades_destacadas.value,
            "motivacion_principal": motivacion_principal.value,
            "descripcion_personal": descripcion_personal.value,
            "horas_semanales": horas_semanales.value,
            "modalidad_de_trabajo": modalidad_de_trabajo.value,
            "experiencia_relevante": experiencia_relevante.value,
            "link_portafolio_cv": link_portafolio_cv.value
        }

        print("✅ Estudiante guardado:")
        for k, v in estudiante_guardado.items():
            print(f"{k}: {v}")

    # Asociar el evento al botón
    boton_enviar.on_click(al_enviar)

    # Mostrar formulario
    formulario = widgets.VBox([
        input_con_etiqueta("nombre_completo", nombre_completo),
        input_con_etiqueta("correo", correo),
        input_con_etiqueta("carrera", carrera),
        input_con_etiqueta("ciclo_actual", ciclo_actual),
        input_con_etiqueta("ubicacion", ubicacion),
        input_con_etiqueta("areas_interes", areas_interes),
        input_con_etiqueta("habilidades_destacadas", habilidades_destacadas),
        input_con_etiqueta("motivacion_principal", motivacion_principal),
        input_con_etiqueta("descripcion_personal", descripcion_personal),
        input_con_etiqueta("horas_semanales", horas_semanales),
        input_con_etiqueta("modalidad_de_trabajo", modalidad_de_trabajo),
        input_con_etiqueta("experiencia_relevante", experiencia_relevante),
        input_con_etiqueta("link_portafolio_cv", link_portafolio_cv),
        boton_enviar
    ])

    display(formulario)