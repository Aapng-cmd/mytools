#!/bin/bash

# this code is a simple example of using arrays
# also, if you are annoyed by ALL your docker containers (or forgot about them), do this

process=($(docker ps | cut -d " " -f 1));

for pr in "${process[@]:1}";
do
  echo "Stopping $pr";
  docker stop $pr;
  docker rm $pr;
  echo "Done";
done
