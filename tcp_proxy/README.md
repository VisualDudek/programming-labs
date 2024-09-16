
`tcp_echo_server/` - docker container, tcp echo server which response with uppercase
    - `docker build -t tcp_echo_server .`
    - `docker run --rm -p 5000:5000 -it tcp_echo_server`

`test/asyncio_tcp_client.py` - test proxy with runing n connections with random lowercase string

`tcp_proxy` - dir with increasing versions of tcp_proxy

Test with:
- `nc`: `nc localhost 5000` or `echo "hello" |nc localhost 5000`
- `telnet`

## Structure

### `tcp_echo_server`
- `001-simple_one_echo.py` - basic echo server.
  - no logs (TODO)-> logging module
  - no configuration -> OOP approach, create Server class and keep config in attributes, NEXT Server class as singleton 
  - no args from cli -> argparse module
  - no loop feat. connection close after one echo -> add loop feat.
  - no concurrency
  - no signal SIGINT handling 
  - no annotation
- `002-x`:
  - added logging module, no print() anymore
  - added Server class, clear structure and explicite server config at class instance initalization
- `003-x`:
  - added loop to handle multiple calls from one client 
  - TODO: DEBUG: try tcpdup `echo "hello" | nc localhost 5000` after this call nc still interactive but server do not get any more calls.
  - added Server static method get_socket_options
  - log server socket options
  - TODO: DEBUG: what each socket option do?