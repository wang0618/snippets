from os import path

from music_dl import config
from music_dl.addons.netease import netease_single

from lib.music.music_api import get_lyric, get_cover
from lib.music.musictag import ID3Tags

import argparse


def download(url, output):
    config.init()
    config.set("cover", False)
    config.set("lyrics", False)
    config.set("verbose", True)

    config.set("outdir", output)
    song = netease_single(url)
    song.download()

    file = path.join(output, song.song_fullname)
    tag = ID3Tags(file)

    tag.title = song.title
    tag.album = song.album
    tag.artist = song.singer
    tag.url = url

    print("Set cover")
    tag.cover = get_cover(song.id)
    if tag.cover:
        print('Set cover succeed')
    print("Set lyric")
    tag.sync_lrc, tag.unsync_lrc = get_lyric(song.id)
    if tag.sync_lrc and tag.unsync_lrc:
        print('Set lyrics succeed')

    tag.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="网易云音乐单曲下载，并补全 MP3 tag (基本信息和歌词)")
    parser.add_argument('url', help="歌曲URL")
    parser.add_argument('--output', '-o', help="输出文件夹", default="./")
    args = parser.parse_args()

    download(args.url, args.output)
