#!/usr/bin/env python3
import argparse
import logging
import sys
import signal
import gi
import json
import requests
import time
import threading
gi.require_version('Playerctl', '2.0')
from gi.repository import Playerctl, GLib

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)


URL = "https://netease-cloud-music-api-zeta-vert.vercel.app"



class GlobalVariable():
    global_track_info = ''
    
    def __init__(self) -> None:
        pass    
    

def download_lyric(track_info):
    logger.info('Download lyric')
    payload = {'keywords': track_info}
    resp = requests.get(url=f"{URL}/search", params=payload)
    id = resp.json()['result']['songs'][0]['id']
    payload = {'id': id}
    resp = requests.get(url=f"{URL}/lyric", params=payload)
    lyric =  resp.json()['lrc']['lyric']
    return lyric


def get_formatted_position(player):
    logger.info('format position')
    position = player.get_position()
    seconds = position // 1000000
    str_min = str(seconds // 60)
    if len(str_min) == 1:
        min_sit = '0' + str_min
    else:
        min_sit = str_min
    str_sec = str(seconds % 60)
    if len(str_sec) == 1:
        sec_sit = '0' + str_sec
    else:
        sec_sit = str_sec
    formatted_time = min_sit + ':' + sec_sit
    return formatted_time


def on_show_lyric(player, metadata, manager, global_track_info, lyric):
    logger.info('show lyric')
    lyric_dic = { item[1:6]: item.split(']')[1] \
        for item in lyric.split('\n') if item != ''}
    while True:
        try:
            track_info = player.get_artist() + ' ' + player.get_title()
        except:
            logger.error('get some error')
            break
        now_position = get_formatted_position(player)
        if global_track_info != track_info:
            sys.stdout.write('\n')
            sys.stdout.flush()
            break
        oneline_lyric = lyric_dic.get(now_position)
        if oneline_lyric is not None:
            sys.stdout.write(oneline_lyric + '\n')
            sys.stdout.flush()
            time.sleep(1.0)
        else:
            time.sleep(1.0)
        

def thread_start(player, metadata, manager):
    logger.info('thread start')
    try:
        track_info = player.get_artist() + ' ' + player.get_title()
        lyric = download_lyric(track_info)
        GlobalVariable.global_track_info = track_info
        global_track_info = GlobalVariable.global_track_info
    except:
        lyric = ''
        global_track_info = ''
        logger.error('get some variable errors')
    x = threading.Thread(target=on_show_lyric, \
                         args=(player, metadata, manager, global_track_info, lyric), daemon=True)
    x.start()


def on_player_appeared(manager, player, selected_player=None):
    if player is not None and (selected_player is None or player.name == selected_player):
        init_player(manager, player)
    else:
        logger.debug("New player appeared, but it's not the selected player, skipping")


def on_player_vanished(manager, player):
    logger.info('Player has vanished')
    sys.stdout.write('\n')
    sys.stdout.flush()


def init_player(manager, name):
    logger.debug('Initialize player: {player}'.format(player=name.name))
    player = Playerctl.Player.new_from_name(name)
    player.connect('metadata', thread_start, manager)
    manager.manage_player(player)
    thread_start(player, player.props.metadata, manager)


def signal_handler(sig, frame):
    logger.debug('Received signal to stop, exiting')
    sys.stdout.write('\n')
    sys.stdout.flush()
    # loop.quit()
    sys.exit(0)



def parse_arguments():
    parser = argparse.ArgumentParser()

    # Increase verbosity with every occurrence of -v
    parser.add_argument('-v', '--verbose', action='count', default=0)

    # Define for which player we're listening
    parser.add_argument('--player')

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    # Initialize logging
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                        format='%(name)s %(levelname)s %(message)s')

    # Logging is set by default to WARN and higher.
    # With every occurrence of -v it's lowered by one
    logger.setLevel(max((3 - arguments.verbose) * 10, 0))

    # Log the sent command line arguments
    logger.debug('Arguments received {}'.format(vars(arguments)))

    manager = Playerctl.PlayerManager()

    loop = GLib.MainLoop()

    manager.connect('name-appeared', lambda *args: on_player_appeared(*args, arguments.player))
    manager.connect('player-vanished', on_player_vanished)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    for player in manager.props.player_names:
        if arguments.player is not None and arguments.player != player.name:
            logger.debug('{player} is not the filtered player, skipping it'
                         .format(player=player.name)
                         )
            continue

        init_player(manager, player)

    loop.run()
    


if __name__ == '__main__':
    main()
