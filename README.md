# 🎹 HandVision Piano: Instrumento Virtual con Computer Vision

Este proyecto transforma tu cámara web en un piano virtual interactivo utilizando Inteligencia Artificial. A diferencia de otros pianos virtuales, este sistema permite tocar una octava completa (notas naturales y sostenidos) mediante el seguimiento de gestos manuales en tiempo real.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-red.svg)

## 🚀 Características Útiles

* **Detección Bi-Manual:** Reconocimiento independiente de la mano izquierda y derecha para cubrir las 8 notas de la octava.
* **Modificador de Sostenidos (Accidentales):** El sistema detecta la posición del pulgar; si está extendido (hacia afuera), las notas cambian a su versión sostenida (`#`).
* **Audio Multi-hilo:** Implementación de `threading` para disparar sonidos sin congelar el flujo de video, garantizando una latencia mínima.
* **Feedback Visual:** Superposición de esqueletos de la mano (landmarks) en tiempo real sobre el video.

## 🛠️ ¿Cómo funciona?

El sistema utiliza **MediaPipe Hands** para mapear 21 puntos de referencia de la mano. 
1. **Detección de Nota:** Se compara la altura (`y`) de la punta del dedo con su base. Si la punta baja de cierto umbral, se dispara la nota.
2. **Lógica de Sostenidos:** Se calcula la posición relativa del pulgar (Nodo 4) respecto al índice (Nodo 5) para determinar si se deben activar las notas sostenidas.
3. **Mapeo de Dedos:**
    * **Mano Izquierda:** Meñique (Do), Anular (Re), Medio (Mi), Índice (Fa).
    * **Mano Derecha:** Índice (Sol), Medio (La), Anular (Si), Meñique (Do octava).


## 📋 Requisitos Previos

* Python 3.8 o superior.
* Cámara web funcional.
* Archivos de audio en formato `.wav` dentro de una carpeta llamada `recursos/`.

## 🔧 Instalación

1.  **Clona este repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/handvision-piano.git](https://github.com/tu-usuario/handvision-piano.git)
    cd handvision-piano
    ```

2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```

## 📂 Estructura del Proyecto

* `main.py`: Código principal con la lógica de visión y audio.
* `recursos/`: Carpeta que debe contener los archivos `.wav` (ej: `do.wav`, `do_sostenido.wav`, etc.).
* `requirements.txt`: Lista de librerías necesarias.


