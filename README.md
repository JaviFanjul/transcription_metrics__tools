## Comparación de Transcripciones

Este proyecto está diseñado para comparar directorios que contienen transcripciones generadas por distintos modelos (por ejemplo, `medium` vs `large`).

> **Importante:** Los archivos `.txt` a comparar deben tener el **mismo nombre** en ambos directorios.
### Scripts disponibles

- **`transcription_comparation.py`**  
  Compara los archivos de texto entre dos directorios y genera un archivo `.csv` con los resultados de la comparación.

- **`metric_representation.py`**  
  Utiliza el archivo `.csv` generado por el script anterior como entrada y crea una carpeta en el directorio raíz con diferentes **gráficos comparativos**.

### Ejemplo de uso

```bash
python transcription_comparation.py
python metric_representation.py
