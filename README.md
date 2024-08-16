<div align="center">
  <h1 align="center">Solucionador de Sistemas de Ecuaciones</a></h1>
</div>

## Ir a la documentacion para la creacion de un entorno virtual
https://docs.python.org/3/library/venv.html

# 👨‍💻 Configuración Local

1. Clona el repositorio bifurcado en tu máquina local.
    ```bash 
    git clone https://github.com/<NOMBRE_DE_USUARIO>/sistemas-de-ecuaciones.git
    ```

3. Navega al directorio del proyecto.
    ```bash
    cd sistemas-de-ecuaciones
    ```

4. Crea un entorno virtual.
    ```bash
    python3 -m venv env
    ```

5. Activa el entorno virtual.
    ```bash
    source env/bin/activate
    ```

6. Instala las dependencias.
    ```bash
    python -m pip install -r requirements.txt
    ```

7. Inicializa el proyecto reflex.
    ```bash
    reflex init
    ```

8. Ejecuta el proyecto.
    ```bash
    reflex run
    ```

*Abre el navegador y ve a `http://localhost:3000/` para ver el proyeco en acción.*

## 🗄️ Estructura de carpetas del sistema de ecuaciones
```bash
|- sistemas_de_ecuaciones
    |- components
      |- fraction.py
      |- fraction_result.py
      |- github_icon.py
    |- styles
      |- styles.py
    |- sistemas_de_ecuaciones.py
    |- state.py
  |- .gitignore
  |- README.md
  |- requirements.txt
  |- rxconfig.py
```

<!-- TechStack -->
## :space_invader: Tecnologias utilizadas
<p align="left">
<a href="https://www.python.org/" target="_blank"><img src="/assets/python.svg" alt="Python" width="150" height="150"/> </a>
<a href="https://reflex.dev/" target="_blank"> <img src="/assets/reflex-light.svg" alt="Reflex" width="150" height="150"/> </a>
</p>

## 👀 Características

- Resolución de sistemas de ecuaciones lineales de hasta 3x3
- Interfaz de usuario intuitiva para ingresar coeficientes y términos independientes
- Visualización gráfica de soluciones para sistemas 2x2 y 3x3
- Opción para generar y resolver sistemas aleatorios
- Resultados mostrados en formato de fracción o decimal

## 🗃️ Estructura del Proyecto

El proyecto está organizado en varios archivos:

1. `state.py`: Contiene la lógica principal y el manejo del estado de la aplicación.
2. `sistemas_de_ecuaciones.py`: Define la interfaz de usuario principal.
3. `styles.py`: Contiene estilos y componentes visuales.
4. `fraction.py` y `fraction_result.py`: Componentes para mostrar fracciones en la UI.

### Desglose de Archivos

#### 🪄 state.py

Este archivo contiene la clase `State` que hereda de `rx.State`. Maneja toda la lógica de la aplicación, incluyendo:

- Almacenamiento y actualización de la matriz de coeficientes y términos independientes
- Resolución del sistema de ecuaciones
- Generación de sistemas aleatorios
- Actualización de la visualización gráfica

Métodos principales:
- `solve_system()`: Resuelve el sistema de ecuaciones ingresado.
- `solve_random()`: Genera y resuelve un sistema aleatorio.
- `update_graph()`: Actualiza la visualización gráfica del sistema.

#### sistemas_de_ecuaciones.py

Define la estructura de la interfaz de usuario utilizando componentes de Reflex. Incluye:

- Campos de entrada para el número de ecuaciones y variables
- Matriz interactiva para ingresar coeficientes
- Botones para resolver, generar sistemas aleatorios y limpiar
- Visualización de resultados y gráficos

#### styles.py

Contiene estilos y componentes visuales, incluyendo:

- `equation_system_graph()`: Componente para mostrar gráficos de Plotly.
- `button_style`: Diccionario de estilos para botones.
- `ondas_effect()`: Efecto visual de fondo (opcional).

#### fraction.py y fraction_result.py

Estos archivos definen componentes para mostrar fracciones en la interfaz de usuario:

- `fraction()`: Componente para mostrar una fracción individual.
- `fraction_result()`: Componente para mostrar los resultados en formato de fracción.

## 🤔 Cómo Usar

1. Ingrese el número de ecuaciones y variables.
2. Haga clic en "Crear matriz" para generar la matriz de entrada.
3. Ingrese los coeficientes y términos independientes.
4. Haga clic en "Resolver" para obtener la solución.
5. Use "Generar y Resolver Aleatorio" para probar con un sistema aleatorio.
6. Cambie entre formato de fracción y decimal con el botón correspondiente.
7. Visualice la solución gráficamente para sistemas 2x2 y 3x3.

## ⚙️ Dependencias

- Reflex
- NumPy
- Plotly

## Notas de Implementación

- La aplicación utiliza NumPy para resolver sistemas de ecuaciones lineales.
- Plotly se usa para generar visualizaciones gráficas interactivas.

## Futuras Mejoras

- Soporte para sistemas de ecuaciones más grandes.
- Más opciones de visualización y análisis.
- Optimización de rendimiento para cálculos complejos.
- Integración con otras herramientas matemáticas.

---
