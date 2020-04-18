import asyncio

import sys
sys.path.append('..')

from game.websocket.server.server_factory import EverythingIsTrumpServerFactory
from game.websocket.server.server_protocol import EverythingIsTrumpServerProtocol


if __name__ == '__main__':
    factory = EverythingIsTrumpServerFactory("ws://127.0.0.1:8765")
    factory.protocol = EverythingIsTrumpServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 8765)
    server = loop.run_until_complete(coro)
    
    print("Created server on localhost:8765")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
