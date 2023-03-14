# Back

Para poder utilizar los siguientes comando se necesita tener instalado *python3-pip*.

## Librerias instaladas con pip.

* fastapi

* uvicorn

* pydantic

* email_validator

* pytest

* coverage


# Iniciar servidor con entorno virtual.

Levantar entorno virtual

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Levantar servidor

    uvicorn main:app --reload

Ejecutar test con coverage

    coverage run -m pytest

    coverage report
