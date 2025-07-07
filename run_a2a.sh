docker build -t multi-agent .
docker run --name multi-agent \
  -p 10019:10019 -p 10020:10020 -p 10021:10021 -p 10022:10022 -p 10023:10023 \
  multi-agent