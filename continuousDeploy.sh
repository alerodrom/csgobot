#!/bin/bash

docker run -d --name csgobot-python \
    -v /home/pomosoft-user/csgobot:/myapp \
        --restart=always \
    --expose=8000 \
    gurken2108/python3-java \
    bash -c "
    echo 'Instalando requirements' && \
    pip install -r requirements.txt && \
    python csgofcNoobsBOT.py "