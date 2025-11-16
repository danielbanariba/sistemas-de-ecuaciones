# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Solucionador de Sistemas de Ecuaciones - A Reflex-based web application for solving systems of linear equations (2x2 to 3x3) with fraction support and 2D/3D visualization.

## Development Commands

```bash
# Setup
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
reflex init

# Run development server (starts at localhost:3000)
reflex run
```

## Architecture

**Framework:** Reflex (Python full-stack framework that generates React frontend)

**Core Pattern:** Reactive State Management

- `resuelvesistema/state.py` - Central `State` class containing all application logic:
  - Matrix operations and input parsing (supports fraction input like "1/2")
  - Linear system solving using NumPy (`np.linalg.solve`, rank calculation)
  - Graph data generation for 2D/3D Plotly visualizations
  - Solution type determination (unique, infinite, no solution)

- `resuelvesistema/resuelvesistema.py` - Main UI definition using Reflex components, connects to State via event handlers

- `resuelvesistema/components/` - Reusable UI components for fraction display and results rendering

- `resuelvesistema/styles/styles.py` - Button styling and Plotly graph component definition

**Key Technologies:**
- NumPy for linear algebra operations
- Plotly for interactive graphing (2D lines, 3D planes)
- Python `fractions` module for exact arithmetic

**Build Artifacts:** `.web/` directory contains auto-generated React/TypeScript frontend (do not edit directly)
