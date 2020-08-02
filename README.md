# 代码片段

`apps` 文件夹为不同的应用类代码，每个应用都有 README.md 说明用法、 requirements.txt 标识依赖.

`lib` 文件夹为共用代码库，被 `apps` 下的代码调用.

## 运行应用

设置PYTHONPATH：

```bash
export PYTHONPATH="$PYTHONPATH:path/to/snippets"
```

在应用目录下直接运行python文件：
 
```bash
python3 xxx.py --help
```

## 应用目录
 
 - [netease_music](./apps/netease_music/): 网易云音乐单曲下载，并补全 MP3 tag (基本信息和歌词)

## Library目录

 - `utils`: 一些工具类
 - `music`:
    - `music_api`: 网易云的搜索、获取封面、歌词的API
    - `musictag`: MP3 tag 编辑  
