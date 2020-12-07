FROM python:3.6
WORKDIR /code
RUN apt-get -qq update 
RUN apt-get install -qq -y python3-pip
RUN pip3 install requests
RUN pip3 install crate
RUN pip3 install geopy
COPY obtenerPosicion.py /code
RUN mkdir /data
CMD ["python3","obtenerPosicion.py"]

