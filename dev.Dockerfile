ARG PYTHON_VERSION=3.7
FROM python:${PYTHON_VERSION}

ENV PATH=/usr/local/bin:${PATH}

WORKDIR /rq
ADD *requirements.txt /rq/

RUN pip install \
                -r requirements.txt \
                -r dev-requirements.txt

ADD . /rq
RUN pip install -e .
