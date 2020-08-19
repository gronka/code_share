#!/bin/sh
sudo docker rm mypostgres
sudo docker build -t mypostgresimage -f ./postgres.dockerfile ./
sudo docker run --name mypostgres mypostgresimage
#sudo docker run -p 5432:5432 --name mypostgres mypostgres
