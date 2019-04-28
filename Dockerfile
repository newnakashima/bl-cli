FROM circleci/python:3.7.3
ENV PYTHONPATH /home/circleci/project
RUN sudo apt install expect
RUN pip install pipenv
CMD test/test.sh
