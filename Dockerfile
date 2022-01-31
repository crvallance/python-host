FROM ubuntu:focal
ENV DEBIAN_FRONTEND=noninteractive
COPY . ./app
RUN apt update && apt install -y tzdata apt-utils && apt install -y bluez python3-pip libbluetooth-dev libboost-python-dev libboost-thread-dev pkg-config python3-dev libglib2.0-dev python3-bluez && python3 -m pip install -r ./app/requirements.txt
ENTRYPOINT python3 /app/service.py
 

