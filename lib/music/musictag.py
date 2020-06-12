"""
require mutagen
"""
from mutagen.id3 import ID3, APIC, USLT, TIT2, TALB, TPE1, SYLT, ID3NoHeaderError, Encoding, PictureType, WXXX


class ID3TagItem:
    def __init__(self, tag_name, getter, setter):
        self.tag_name = tag_name
        self.getter = getter
        self.setter = setter

    def __get__(self, obj: "ID3Tags", type=None):
        items = obj.tag.getall(self.tag_name)
        if len(items) >= 1:
            return self.getter(items[0])
        return None

    def __set__(self, obj: "ID3Tags", value) -> None:
        if value:
            obj.tag.setall(self.tag_name, [self.setter(value)])


class ID3Tags:
    title = ID3TagItem('TIT2', lambda i: i.text[0], lambda i: TIT2(encoding=Encoding.UTF8, text=i))
    album = ID3TagItem('TALB', lambda i: i.text[0], lambda i: TALB(encoding=Encoding.UTF8, text=i))
    artist = ID3TagItem('TPE1', lambda i: i.text[0], lambda i: TPE1(encoding=Encoding.UTF8, text=i))
    sync_lrc = ID3TagItem('SYLT', lambda i: i.text,
                          lambda i: SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=i))
    unsync_lrc = ID3TagItem('USLT', lambda i: i.text, lambda i: USLT(encoding=Encoding.UTF8, lang='eng', text=i))
    url = ID3TagItem('WXXX', lambda i: i.url, lambda i: WXXX(encoding=Encoding.UTF8, url=i))
    cover = ID3TagItem('APIC', lambda i: i.data, lambda i: APIC(
        encoding=Encoding.LATIN1,  # if other apple music/itunes  can't display img
        mime='image/jpeg',  # image/jpeg or image/png
        type=PictureType.COVER_FRONT,
        data=i))

    def __init__(self, mp3path):
        self.file_path = mp3path
        try:
            self.tag = ID3(mp3path)
        except ID3NoHeaderError:
            self.tag = ID3()

    def save(self, file_path=None):
        file_path = file_path or self.file_path
        self.tag.save(file_path or self.file_path, v2_version=3)
