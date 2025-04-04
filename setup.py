from setuptools import setup, find_packages

setup(
    name="personal-memo-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "sqlalchemy==2.0.27",
        "mysql-connector-python==8.3.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.9",
        "redis==5.0.1",
        "pandas==2.2.0",
        "matplotlib==3.8.2",
        "python-dotenv==1.0.1",
        "pytest==8.0.0",
        "alembic==1.15.2",
        "pydantic-settings==2.3.0",
        "email-validator==2.2.0",
    ],
) 