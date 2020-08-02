"""
MacOS中，将歌曲文件加入itunes，使用网易云客户端同步itunes音乐并匹配音乐后，
即可使用本脚本将网易云匹配到的音乐信息写入音乐文件
"""

import argparse
import getpass
import shutil
import sqlite3
from os import path

from lib.music.music_api import get_lyric, get_cover
from lib.music.musictag import ID3Tags

db_file = "/Users/{user}/Library/Containers/com.netease.163music/Data/Documents/storage/sqlite_storage.sqlite3".format(
    user=getpass.getuser())


def get_musics(music_dir):
    """
    :param music_dir:
    :return: [(file, tid, title, album, artist), ...]
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("select file, tid, title, album, artist from track")
    return [
        i
        for i in cursor.fetchall()
        if i[0].startswith(music_dir) and i[1]
    ]


def tag_files(music_dir, output_dir=None):
    for file, tid, title, album, artist in get_musics(music_dir):
        print('Processing %s' % file)

        artist = artist.strip(',')

        tag = ID3Tags(file)

        tag.title = title
        tag.album = album
        tag.artist = artist
        tag.url = 'https://music.163.com/#/song?id=%s' % tid

        tag.cover = get_cover(tid)
        if not tag.cover:
            print('\tSet cover failed')
        tag.sync_lrc, tag.unsync_lrc = get_lyric(tid)
        if not tag.sync_lrc and not tag.unsync_lrc:
            print('\tSet lyrics failed')

        tag.save()

        if output_dir:
            outfile = path.join(output_dir, '%s - %s.mp3' % (artist, title))
            try:
                shutil.move(file, outfile)
                print('\tMove to %s' % outfile)
            except Exception as e:
                print('\tMove to %s error:%s' % (output_dir, e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="网易云iTunes音乐MP3 tag补全")
    parser.add_argument('--dir', '-d', help="文件夹过滤，只处理指定文件夹下的文件", default='/')
    parser.add_argument('--output', '-o', help="输出文件夹(不指定则不将补全的音乐文件移动)", default=None)
    args = parser.parse_args()

    music_dir = path.abspath(args.dir)

    tag_files(music_dir, output_dir=args.output)
    # res = get_musics(music_dir)
