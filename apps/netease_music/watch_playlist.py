"""
监控歌单歌曲增加，并下载之

通过输出目录下的 last_download_id.log 文件记录已经下载好的歌单最新歌曲id
"""
from music_dl import config

config.init()

import argparse
from os import path
from music_dl.addons.netease import netease_playlist
from netease_single_download import download

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="网易云音乐歌单下载")
    parser.add_argument('url', help="歌单URL")
    parser.add_argument('--output', '-o', help="输出文件夹", default="./")
    args = parser.parse_args()

    mlist = netease_playlist(args.url)
    mids = [m.id for m in mlist]

    try:
        last_download_id = int(open(path.join(args.output, 'last_download_id.log')).read())
        print('From id %s' % last_download_id)
    except Exception:
        last_download_id = 0

    if last_download_id in mids:
        pos = mids.index(last_download_id)
        mlist = mlist[:pos]

    for m in mlist:
        print('Downloading %s from https://music.163.com/#/song?id=%s' % (m.title, m.id))
        try:
            download('https://music.163.com/#/song?id=%s' % m.id, args.output)
        except Exception as e:
            print('Downloading %s error:%s' % (m.title, e))

    if mids:
        open(path.join(args.output, 'last_download_id.log'), 'w').write(str(mids[0]))
