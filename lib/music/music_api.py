"""
require requests
"""
import re
from collections import namedtuple

import requests

Song = namedtuple('Song', 'id name artists album image')

netease_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  # noqa
    "Accept-Charset": "UTF-8,*;q=0.5",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",  # noqa
    "referer": "https://www.google.com",
}


def search(s):
    data = {
        's': s,
        'offset': 0,
        'limit': 10,
        'type': 1
    }

    r = requests.post('http://music.163.com/api/search/pc', data=data, timeout=10, headers=netease_headers)
    # print(json.dump(r.json(), open('out.json', 'w'), indent=4, ensure_ascii=False))
    res_ = r.json()
    if res_['code'] != 200 or res_['result']['songCount'] == 0:
        return False

    songs = []
    for song in res_['result']['songs']:
        songs.append(Song(
            song['id'],
            song['name'],
            ','.join(i.get('name', '') for i in song['artists']),
            song.get('album', {}).get('name', ''),
            song.get('album', {}).get('picUrl', ''),
        ))

    return songs


def get_lyric(id, include_trans=True):
    """返回带时间轴和纯文本歌词"""
    r = requests.get('http://music.163.com/api/song/lyric?os=pc&id=%s&lv=-1&kv=-1&tv=-1' % id, timeout=10,
                     headers=netease_headers)
    res = r.json()
    # print(res)
    if res.get('nolyric'):
        return [], ''

    lrc_text = res['lrc']['lyric'].strip()
    if include_trans:
        lrc_text += '\n' + (res['tlyric'].get('lyric') or '').strip()
    # print(lrc_text)
    sync_lrc = []
    for line in lrc_text.splitlines():
        """
        歌词的形式：
            [00:00.000] 作曲 : 宋冬野
            [00:17][00:32]Say you, say me
        """
        times = []  # 歌词时间点
        patten = r'\[(?P<minute>[0-9].*?):(?P<second>[0-9].*?)(.(?P<millisecond>[0-9].*?))?\](?P<text>.*)'
        while 1:
            match = re.search(patten, line)
            if match:
                min, sec, mil = match.group('minute'), match.group('second'), match.group('millisecond')
                t = (int(min) * 60 + int(sec)) * 1000 + int(mil or 0) * 10
                times.append(t)
                line = match.group('text')
            else:
                break

        if times:
            sync_lrc.extend([line, t] for t in times)

    sync_lrc.sort(key=lambda i: (i[1], i[0]))
    unsync_lrc = '\n'.join(line[0] for line in sync_lrc)
    return sync_lrc, unsync_lrc


def get_cover(id):
    res = requests.get('http://music.163.com/api/song/detail/', params={'id': id, 'ids': '[%s]' % id},
                       timeout=10, headers=netease_headers)
    img = res.json()['songs'][0]['album']['picUrl']
    return requests.get(img).content


if __name__ == '__main__':
    # s = search('CANNIE(晴子)')
    # print(s)
    lrc = get_lyric('28396861')
    print(lrc)
