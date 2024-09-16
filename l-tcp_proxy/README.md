
`tcp_echo_server/` - docker container, tcp echo server which response with uppercase
    - `docker build -t tcp_echo_server .`
    - `docker run --rm -p 5000:5000 -it tcp_echo_server`

`test/asyncio_tcp_client.py` - test proxy with runing n connections with random lowercase string

`tcp_proxy` - dir with increasing versions of tcp_proxy

