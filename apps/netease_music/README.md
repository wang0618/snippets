# 网易云脚本

使用 `python <script> --help` 查看脚本选项

## netease_single_download.py

网易云单曲下载，自动补全歌曲Tag信息（歌曲名、专辑、作者、封面、歌词）

## watch_playlist.py

下载网易云歌单最近增加的歌曲。

实现了自动去重，定时运行本脚本可实现即时下载歌单歌曲，以防歌曲变灰

## tag_itunes.py

为MacOS上导入网易云的itunes音乐文件添加歌曲Tag信息（歌曲名、专辑、作者、封面、歌词）。歌曲Tag信息根据网易云的匹配音乐信息来完善。

MacOS中，将歌曲文件加入itunes，使用网易云客户端同步itunes音乐并匹配音乐后，即可使用本脚本将网易云匹配到的音乐信息写入音乐文件