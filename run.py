#!/usr/bin/env python3
"""
Entry point for the Zombie IoT Sensor Simulation.
Run this script to start the application.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import ZombieSimulationCLI

if __name__ == "__main__":
    app = ZombieSimulationCLI()
    app.run() 