import asyncio

import sys
sys.path.append('..')

from game.websocket.server.server_factory import EverythingIsTrumpServerFactory
from game.websocket.server.server_protocol import EverythingIsTrumpServerProtocol


if __name__ == '__main__':
    factory = EverythingIsTrumpServerFactory("ws://0.0.0.0:80")
    factory.protocol = EverythingIsTrumpServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 80)
    server = loop.run_until_complete(coro)
    
    print("Created server on port 80")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
