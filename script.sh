#/bin/bash

while :
do
  echo "Crawling weather"
  docker run --rm capstone-spider python spider.py --host host.docker.internal --city Copenhagen
  docker run --rm capstone-spider python spider.py --host host.docker.internal --city Bergen
  docker run --rm capstone-spider python spider.py --host host.docker.internal --city Stockholm
  echo "Going to sleep"
  sleep 60
done