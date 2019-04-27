FROM circleci/python:3.7.3
ADD . /code
WORKDIR /code
ENV PYTHONPATH /code
RUN sudo apt install expect
RUN pip install pipenv
RUN sudo pipenv install
CMD test/test.sh
