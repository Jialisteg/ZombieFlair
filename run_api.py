#!/usr/bin/env python
"""
Script para iniciar el servidor API de FastAPI para la Simulación de Zombies.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=5000, reload=True) 