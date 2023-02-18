import sys
import requests
import time
import gi
import argparse
import threading
gi.require_version('Playerctl', '2.0')
from gi.repository import Playerctl

# personal netease music api
URL = "https://netease-cloud-music-api-zeta-vert.vercel.app"
# flag to control change lyric
global_track_info = ''


def download_lyric(track_info):
    """
    dowload lyric meanwhile change global_track_info to the new one.
    """
    global global_track_info
    global_track_info = track_info
    payload = {'keywords': track_info}
    resp = requests.get(url=f"{URL}/search", params=payload)
    id = resp.json()['result']['songs'][0]['id']
    payload = {'id': id}
    resp = requests.get(url=f"{URL}/lyric", params=payload)
    lyric =  resp.json()['lrc']['lyric']
    return lyric


def get_track_info(player):
    track_info = player.get_artist() + ' ' + player.get_title()
    return track_info


def get_formatted_position(player):
    """
    get player's formatted position, to match lyric timeline(
    like: 01:01 means process 1 minute 1 second from music start)
    """
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


def show_lyric(track_info, lyric, player):
    """
    print lyric line by line, if new track_info is different from 
    global_track_info, break the infinite loop.
    """
    global global_track_info
    lyric_dic = { item[1:6]: item.split(']')[1] \
        for item in lyric.split('\n') if item != ''}
   
    now_position = get_formatted_position(player)
    while True:
        if global_track_info != track_info:
            break
        oneline_lyric = lyric_dic.get(now_position)
        if oneline_lyric is not None:
            sys.stdout.write(oneline_lyric + '\n')
            sys.stdout.flush()
            time.sleep(0.1)
            now_position = get_formatted_position(player)
        else:
            time.sleep(0.1)
            now_position = get_formatted_position(player)


def start_thread(track_info, lyric, player):
    """
    new thread to run show_lyric function.
    """
    x = threading.Thread(target=show_lyric, args=(track_info, lyric, player), daemon=True)
    x.start()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--player')
    return parser.parse_args()


if __name__ == '__main__':
    while True:
        arguments = parse_arguments()
        manager = Playerctl.PlayerManager()
        for player_name in manager.props.player_names:
            if arguments.player is not None and arguments.player != player_name.name:
                continue
        try:
            player = Playerctl.Player.new_from_name(player_name)
            track_info = get_track_info(player)
            # compare global_track_info with new track_info, if has different download the new lyric.
            if global_track_info != track_info or global_track_info == '':
                lyric = download_lyric(track_info)
                start_thread(track_info, lyric, player)
            else:
                time.sleep(0.2)
        # incase no player.
        except NameError:
            time.sleep(1.0)
        except KeyboardInterrupt:
            break
