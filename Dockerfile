FROM python:3.8-buster
RUN useradd --create-home api
USER api
WORKDIR /home/api
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 5000
COPY requirements.txt ./
RUN python3 -m venv venv
ENV PATH="/home/api/venv/bin:$PATH"
RUN pip install -r requirements.txt
COPY  main.py ./
CMD ["flask", "run"]