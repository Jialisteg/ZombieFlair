from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="zombies-iot-simulation",
    version="1.0.0",
    author="JavierAliste",
    author_email="jialisteg@gmail.com",
    description="Simulación de Sensores IoT con Zombis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/zombie-iot-simulation",
    packages=find_packages(),
    package_data={
        "": ["config.yaml"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "zombie-sim=src.run:main",
        ],
    },
) 