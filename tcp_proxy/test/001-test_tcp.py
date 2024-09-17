#!/bin/env python3

import asyncio
import random
import string
import argparse

async def tcp_echo_client(message):
    try: 
        # port = random.choice([5001, 5200, 5300])
        host = '127.0.0.1'
        port = 5000
        # host = 'tcp-echo.fly.dev'
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=1.5)

        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()

        try:
            data = await asyncio.wait_for(reader.read(100), timeout=2.0)
            print(f'Received: {data.decode()!r}')
        except asyncio.TimeoutError:
            print('Timeout Error on read')

        print('Close the connection')
        writer.close()
        await writer.wait_closed()

    except asyncio.TimeoutError:
        print('Timeout Error on connection')

def get_random_sting(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

async def run_multiple_clients(n):
    # await asyncio.gather(
    #     tcp_echo_client('Hello World!'),
    #     tcp_echo_client('Goodbye World!'),
    # )
    messages = [get_random_sting() for _ in range(n)] 
    tasks = (tcp_echo_client(message) for message in messages)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
# asyncio.run(tcp_echo_client('Hello World!'))
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=10, help='number of clients')
    args = parser.parse_args()

    asyncio.run(run_multiple_clients(n=args.n))