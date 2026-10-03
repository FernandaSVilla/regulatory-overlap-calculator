# Regulatory Overlap Calculator (v1.0)

Importe mínimo rentable y coste de la superposición regulatoria en la IA bancaria.

Calculadora, datos y código reproducibles del ensayo *Simplificar sin desproteger* (V Premio Federico Prades-IEBF 2026).

| Carpeta | Contenido |
|---|---|
| `calculadora/index.html` | Calculadora del importe mínimo rentable. Se abre en cualquier navegador; no guarda ni envía datos. |
| `datos/matriz_obligaciones_v1.csv` | 50 obligaciones codificadas (decisión, marco, artículo, función, fase, evidencia). |
| `datos/relaciones_v1.csv` | 32 relaciones entre obligaciones de marcos distintos: I equivalente, D definición distinta, C en tensión, N integrada por norma expresa. |
| `codigo/matriz.py` | Calcula los índices de superposición, divergencia e integración (secciones 4.1 y 4.2). |
| `codigo/modelos.py` | Coste por modelo, importe mínimo rentable, sensibilidad, Monte Carlo (semilla 2026) y simulación de monocultura (secciones 4.3, 4.4 y 4.6). Requiere Python 3 y NumPy. |

## Reproducir los resultados

```
cd codigo
python3 matriz.py
python3 modelos.py
```

`modelos.py` lee la matriz para derivar el descuento por integración, así que ejecútalo desde `codigo/` después de ajustar las rutas si cambias la estructura.

## Libro de códigos

Ver anexo A del ensayo. La matriz es la versión 1.0 (3.10.2026). Las correcciones se publicarán como nuevas versiones con su propio DOI.

## Licencia y cita

| Parte | Licencia | Archivo |
|---|---|---|
| Código: `calculadora/`, `codigo/`, `visualizacion/` | Apache License 2.0 | `LICENSE` |
| Datos: `datos/` | CC BY 4.0 | `LICENSE-DATA` |

Cita la versión exacta que uses (archivo `CITATION.cff`).

## Visualización

La carpeta `visualizacion/` contiene el script de Python (Matplotlib) con el que se elaboraron los gráficos del ensayo a partir de la matriz y de los modelos. Permite reproducirlos y comprobar que coinciden con las cifras del texto: `cd visualizacion && python3 graficos.py`.
