import os.path
import socket
import logging
import argparse

from twisted.internet import reactor
from twisted.web import server, static

from autobahn.twisted.resource import WebSocketResource

from rose.common import config
from . import game, net

log = logging.getLogger("main")


def main():
    logging.basicConfig(level=logging.INFO, format=config.logger_format)
    parser = argparse.ArgumentParser(description="ROSE Server")
    parser.add_argument(
        "--track_definition",
        "-t",
        dest="track_definition",
        default="random",
        choices=["random", "same"],
        help="Definition of driver tracks: random or same."
             "If not specified, random will be used.",
    )
    parser.add_argument(
        "--track_file_read",
        "-r",
        dest="track_file_read",
        default="",
        help="path of track data file.",
    )
    parser.add_argument(
        "--track_file_write",
        "-w",
        dest="track_file_write",
        default="",
        help="path of track data file.",
    )

    args = parser.parse_args()
    """
    If the argument is 'same', the track will generate the obstacles in the
    same place for both drivers, otherwise, the obstacles will be genrated in
    random locations for each driver.
    """
    if args.track_definition == "same":
        config.is_track_random = False
    else:
        config.is_track_random = True

    if args.track_file_read != "":
        config.track_file_name_read = args.track_file_read
        file_exist = os.path.isfile(args.track_file_read)

        if file_exist:
            config.track_file_name_read = True

    if args.track_file_write != "":
        config.track_write_mode = True
        config.track_file_name_write = args.track_file_write

    log.info("starting server")
    g = game.Game()
    h = net.Hub(g)
    reactor.listenTCP(config.game_port, net.PlayerFactory(h))
    root = static.File(config.web_root)
    wsuri = "ws://%s:%s" % (socket.gethostname(), config.web_port)
    watcher = net.WatcherFactory(wsuri, h)
    root.putChild(b"ws", WebSocketResource(watcher))
    root.putChild(b"res", static.File(config.res_root))
    root.putChild(b"admin", net.WebAdmin(g))
    root.putChild(b"rpc2", net.CliAdmin(g))
    site = server.Site(root)
    reactor.listenTCP(config.web_port, site)
    reactor.run()
