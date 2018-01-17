# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from time import clock
from .compat import urlopen
import sys

class Video(object):
    def __init__(self, url, video_logo,video_name, extension, definition=None,
                 video_codec=None, profile=None, video_bitrate=None,
                 audio_codec=None, audio_bitrate=None):
        self.url = url
        self.video_logo = video_logo
        self.video_name = video_name
        self.extension = extension
        self.definition = definition
        self.video_codec = video_codec
        self.profile = profile
        self.video_bitrate = video_bitrate
        self.audio_codec = audio_codec
        self.audio_bitrate = audio_bitrate

    def __repr__(self):
        """类实例表示。"""
        return '<Video: (.{0})-{1}>'.format(
            self.extension, self.definition)

    def __lt__(self, other):
        """（lt）（）方法用于比较视频对象
        这在排序时很有用。
         ：param其他：
             另一个视频实例的实例进行比较。
        """
        if isinstance(other, Video):
            v1 = '{0} {1}'.format(self.extension, self.definition)
            v2 = '{0} {1}'.format(other.extension, other.definition)
            return (v1 > v2) - (v1 < v2) < 0

    # 暴露在外在api接口：返回过滤后的url地址
    def get_video_url(self):
        return self.url

    # 暴露在外在api接口：返回爬取视频的封面图地址
    def get_logo_url(self):
        return self.video_logo

    # 暴露在外在api接口：下载
    def download(self, path, chunk_size=8 * 1024, on_progress=None,
                 on_finish=None, force_overwrite=False):
        """下载视频
         ：param str路径：
             目的地输出目录。model.py
         ：param int chunk_size：
             一次写入缓冲区的文件大小（以字节为单位）。 默认，
             这被设置为8个字节。
         ：param func on_progress：
             *可选*函数在每次写入缓冲区时被调用
             至。 传递的参数是接收的字节数，文件大小和开始
             约会时间。
         ：param func on_finish：
             *可选*下载完成后的回调函数。参数
             传递的是完整路径下载的文件。
         ：param bool force_overwrite：
             *可选*如果存在冲突的话，强制文件覆盖。
        """
        path = os.path.normpath(path)
        if not os.path.isdir(path):
            raise OSError('Make sure path exists.')

        video_name = '{0}.{1}'.format(self.video_name, self.extension)
        path = os.path.join(path, video_name)
        if os.path.isfile(path) and not force_overwrite:
            raise OSError("Conflicting video_name:'{0}'".format(self.video_name))

        response = urlopen(self.url)
        file_size = self.file_size(response)
        self._bytes_received = 0
        start = clock()
        try:
            with open(path, 'wb') as dst_file:
                while True:
                    self._buffer = response.read(chunk_size)
                    # 检查缓冲区是否为空（也称没有字节剩余）。
                    if not self._buffer:
                        if on_finish:
                            #  `_bytes_recieved``缓冲区之前我们调用
                            #  ``on_finish（）``。
                            on_finish(path)
                        break

                    self._bytes_received += len(self._buffer)
                    dst_file.write(self._buffer)
                    if on_progress:
                        on_progress(self._bytes_received, file_size, start)

        except KeyboardInterrupt:
            # 还应该允许你禁用这个。
            os.remove(path)
            raise KeyboardInterrupt(
                'Interrupt signal given. Deleting incomplete video.')

    def file_size(self, response):
        """从响应中获取文件大小
           
        :param response: 打开的URL的响应。
        :return:
        """
        meta_data = dict(response.info().items())
        return int(meta_data.get('Content-Length') or
                   meta_data.get('content-length'))
