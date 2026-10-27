import os
import requests
from typing import List
import datetime
import urllib.parse

def optimizar_prompt(query: str) -> str:
    """
    Herramienta para validar y optimizar la petición del usuario, 
    añadiendo el estilo de robots Gundam / Mecha.
    """    
    # Tags de calidad
    tags_calidad = "masterpiece, best quality, detailed, "
    
    # Tags específicos
    tags_estilo = (
        "giant mecha, mobile suit, gundam style, japanese anime robot, sci-fi, "
        "mechanical parts, panel lines, glowing eyes, V-fin antenna, metallic texture, "
        "dynamic pose, hangar background, "
    )
    
    tags_usuario = query.strip().lower()
    
    prompt_final = f"{tags_calidad}{tags_estilo}{tags_usuario}"
    return prompt_final

def generar_imagen_nube(prompt_optimizado: str, nombre_archivo: str = "") -> str:
    """
    Herramienta que se conecta a Pollinations.ai para generar una imagen basada en un prompt.
    
    Args:
        prompt_optimizado: str -> El prompt detallado en inglés.
        nombre_archivo: str -> (Opcional) Nombre base para el archivo. Si no se provee, se usa la fecha y hora.
    """
    if "ERROR" in prompt_optimizado:
        return "No se puede generar la imagen porque el prompt no es válido."

    try:
        prompt = urllib.parse.quote(prompt_optimizado)
        url = f"https://image.pollinations.ai/prompt/{prompt}"
        
        response = requests.get(url, timeout=60) 
        
        if response.status_code != 200:
            return f"Error en la API de imágenes (Código {response.status_code})."
            
        if not response.content:
            return "Error: La API devolvió una respuesta vacía."

        os.makedirs("imagenes_generadas", exist_ok=True)
        
        # Genera un timestamp único
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not nombre_archivo or nombre_archivo in ["resultado", "gundam", "imagen"]:
            nombre_final = f"gundam_{timestamp}"
        else:

            nombre_limpio = "".join(c for c in nombre_archivo if c.isalnum() or c in "_-").strip()
            nombre_final = f"{nombre_limpio}_{timestamp}"
            
        ruta = f"imagenes_generadas/{nombre_final}.png"
        
        with open(ruta, "wb") as f:
            f.write(response.content)
            
        return f"Éxito. La imagen se descargó en tu computadora con el nombre {nombre_final}.png. Revisa tu carpeta local 'imagenes_generadas'."
        
    except requests.exceptions.Timeout:
        return "Error: La generación de la imagen tardó demasiado tiempo (Timeout)."
    except Exception as e:
        return f"Error interno en generación: {str(e)}"

def listar_imagenes_generadas() -> List[str]:
    """
    Herramienta para listar las imágenes .png generadas previamente en la carpeta de imágenes.
    ÚSALA SIEMPRE que el usuario pregunte qué imágenes tienes, pida ver la lista de imágenes, 
    o pregunte qué robots ha creado hasta ahora. 
    Devuelve una lista con los nombres de los archivos .png guardados.
    """
    try:
        carpeta = "imagenes_generadas"
        if not os.path.exists(carpeta):
            return ["No se encontró la carpeta de imágenes. Aún no has generado ninguna."]
            
        archivos = [f for f in os.listdir(carpeta) if f.endswith('.png')]
        
        # VALIDACIÓN: Resultados vacíos
        if not archivos:
            return ["No se encontraron imágenes generadas en la carpeta."]
            
        return [f"Archivo: {a}" for a in archivos]
    except Exception as e:
        return [f"Error al leer archivos: {str(e)}"]