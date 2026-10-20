# Regulatory Overlap Calculator

[![Código: Apache 2.0](https://img.shields.io/badge/c%C3%B3digo-Apache%202.0-blue.svg)](LICENSE) [![Datos: CC BY 4.0](https://img.shields.io/badge/datos-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)

Una calculadora y una matriz abiertas para medir cuánto se superponen las normas europeas que regulan las decisiones automatizadas de un banco, cuánto cuesta cumplirlas a la vez y a quién deja fuera ese coste.

**Calculadora en línea →** [fernandasvilla.github.io/regulatory-overlap-calculator](https://fernandasvilla.github.io/regulatory-overlap-calculator/calculadora/)  
**Mapa en línea →** [fernandasvilla.github.io/regulatory-overlap-map](https://fernandasvilla.github.io/regulatory-overlap-map/)

---

## De qué trata

Cuando varias normas europeas (el Reglamento de IA, el RGPD, la Directiva de crédito al consumo, el AMLR y DORA) regulan la misma decisión de un banco, ¿cuánto cuesta cumplirlas a la vez y a quién deja fuera ese coste? Trabajé con dos decisiones que vive cualquier cliente: **abrir una cuenta** y **pedir un crédito al consumo**.

El hallazgo central: el legislador ya permite que el banco cumpla una sola vez buena parte de sus obligaciones internas, pero no ha hecho lo mismo con lo que la persona tiene derecho a pedir, como la revisión humana, la explicación o la comunicación de la denegación.

## Qué hay en cada carpeta

**`calculadora/`**. Una página web que calcula cuánto suben los costes regulatorios el importe mínimo a partir del cual un préstamo al consumo le sale rentable a una entidad. Se puede cambiar cada supuesto (tipo de interés, tamaño de la entidad, cómo se revisan las denegaciones...) y ver el efecto al momento. Se abre en cualquier navegador y no guarda ni envía ningún dato.

**`datos/`**. La matriz que construí codificando 50 obligaciones de esas normas y las 32 relaciones entre ellas. Cada relación lleva un código: I (equivalente), D (misma finalidad, definición distinta), C (en tensión) o N (integrada por una norma expresa). Las reglas de codificación están en `datos/libro_de_codigos_v1.2.md`. La versión vigente es la 1.2, congelada el 14 de octubre de 2026: las relaciones están en `matriz_relaciones_v1.2_congelada_2026-10-14.csv` y las obligaciones en `matriz_obligaciones_v1.1.csv`, que no cambió. Los demás archivos se conservan como versiones anteriores.

**`codigo/`**. Dos scripts de Python. `matriz.py` calcula los índices de superposición e integración. `modelos.py` calcula el coste por préstamo, el importe mínimo rentable, el análisis de sensibilidad, la simulación de Monte Carlo y la simulación de monocultura.

**`visualizacion/`**. `graficos.py`, el script que dibuja los gráficos a partir de los datos, y las imágenes que genera. Los gráficos de la matriz y de los modelos se calculan dentro del propio script; los datos de los demás (el calendario de aplicación de las normas, las cuentas de pago básicas rechazadas por país, los estados del alta de cuenta y la posición de cada punto en la red de obligaciones) están en `visualizacion/datos_figuras/`.

## Cómo reproducir los resultados

Necesitas Python 3 con NumPy y Matplotlib.

```
cd codigo
python3 matriz.py
python3 modelos.py

cd ../visualizacion
python3 graficos.py
```

Las simulaciones usan una semilla fija (2026), así que cada vez que las ejecutes obtendrás exactamente las mismas cifras.

## Límites

Los costes y los perfiles de entidad son supuestos razonados a partir de fuentes públicas, no datos medidos dentro de los bancos. Por eso existe la calculadora: para que cada quien ponga sus propios números. La codificación de la matriz la hice yo, y un jurista independiente la codificó a ciegas como prueba de fiabilidad. Si encuentras un error o no estás de acuerdo con algún código, me ayudaría mucho que abrieras un *issue*.

## Licencia y cómo citar

El código (`calculadora/`, `codigo/`, `visualizacion/`) se publica con licencia Apache 2.0 y los datos (`datos/` y `visualizacion/datos_figuras/`) con CC BY 4.0. Si usas algo de aquí, cita la versión exacta que hayas usado. También puedes usar el botón **«Cite this repository»** de esta página, que genera la cita en APA y BibTeX a partir de `CITATION.cff`.

**Cómo citar**

> Sánchez-Villa, M. F. (2026). *Regulatory Overlap Calculator: obligations matrix and cost model for automated credit and account-opening decisions* (Version 1.1.0) [Software and data]. GitHub. https://github.com/FernandaSVilla/regulatory-overlap-calculator
