# Create docker container

``` sudo docker buildx build --platform linux/arm64 -t c0n7z3r0/fritzhome-cli:k3s-arm64 --push .```

# Command to run container 

```sudo docker run c0n7z3r0/fritzhome-cli -f [fritz-box_ipv4] -u api -p [PASSWORD] writelongterminflux -org [influxDB-ORG] -url [influxdb-ipv4]:8086 -bucket [influxDB-ORG-bucket] -token [TOKEN]```
