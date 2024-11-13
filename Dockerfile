FROM nanoowl:23-01

COPY ./nanoowl /nanoowl
RUN pip install loguru uvicorn fastapi && pip install -U pydantic
RUN cd /nanoowl && python setup.py develop --user
