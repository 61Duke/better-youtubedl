# -*- coding: utf-8 -*-
class MultipleObjectsReturned(Exception):
    """当预期只有一个对象时，该查询返回了多个对象。
    """
    pass


class ExtractorError(Exception):
    """某些特定于js解析器的内容失败。
    """


class YoutubeDlError(Exception):
    """特定于包装器失败了。
    """
    pass


class CypherError(Exception):
    """_cipher方法返回错误。
    """
    pass


class DoesNotExist(Exception):
    """所请求的视频不存在。
    """
    pass


class AgeRestricted(Exception):
    """所请求的视频有年龄限制。
    """
    pass
