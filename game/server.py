import asyncio

from server_factory import EverythingIsTrumpServerFactory
from server_protocol import EverythingIsTrumpServerProtocol


if __name__ == '__main__':
    factory = EverythingIsTrumpServerFactory("ws://0.0.0.0:8080")
    factory.protocol = EverythingIsTrumpServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 8080)
    server = loop.run_until_complete(coro)
    
    print("Created server on port 8080")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
