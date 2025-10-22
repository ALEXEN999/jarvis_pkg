# Contribuir

## Requisitos
- Python 3.10+
- `pip install -r requirements.txt`

## Estilo
- Formato: Black
- Lint: Ruff
- Pre-commit (opcional): `pre-commit install`

## Flujo de trabajo (git)
1. `git checkout -b feat/mi-cambio`
2. Cambios + tests locales
3. `ruff check .` y `black .`
4. `git commit -m "feat: descripción corta"`
5. PR a `main`

## Tests manuales
- Escritura/lectura/listado en Escritorio
- Comando de shell benigno (`echo`)
- Rutas fuera de SAFE_ROOTS → deben bloquearse
