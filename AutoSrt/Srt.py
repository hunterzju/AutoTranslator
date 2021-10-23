class SrtItem:
    __slots__ = ['index', 'timeline', 'content']
    def __init__(self, idx=None, timeline=None, content=None):
        self.index = idx
        self.timeline = timeline
        self.content = content

    def setIdx(self, idx):
        self.index = idx

    def setTimeline(self, timeline):
        self.timeline = timeline

    def setContent(self, content):
        self.content = content

class SrtPage:
    def __init__(self, lang=None, srt_list=[]):
        self.language = lang
        self.srt_list = srt_list

    def appendSrt(self, srt_item):
        # FIXME: checkif self.srt_list is 'list' type
        self.srt_list.append(srt_item)
