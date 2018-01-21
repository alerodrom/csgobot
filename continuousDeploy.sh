#!/bin/bash

docker run -d --name csgobot-python \
	-v "/home/pomosoft-user/csgobot":/myapp \
 	-w /myapp \
    --restart=always \
	--expose=5000 \
    gurken2108/python3-java
    bash -c "
    echo 'Instalando requirements' && \
    pip install -r requirements.txt && \
    bash runBOT.sh"