from setuptools import setup, find_packages

setup(
    name="weather-crew-app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.2",
        "crewai==0.83.0",
        "langchain>=0.2.16",
        "python-dotenv==1.0.0",
    ],
)
