# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import logging
import re
from collections import defaultdict
from .exceptions import YoutubeDlError, AgeRestricted, CypherError
from .compat import urlopen, unquote
from .quality_constant import QUALITY_PROFILE_KEYS, QUALITY_PROFILES
from .jsinterp import JSInterpreter
from .utils import safe_filename
from .model import Video


log = logging.getLogger(__name__)


class Better_Youtube_Downloader(object):
    """
    锁定Youtube下载内容的单例实例
    """

    def __init__(self, url=None):
        """
        初始化Better_Youtube_Downloader中内容和api封装
        """
        self._title = None
        self._filename = None
        self._video_url = url
        self._js_cache = []
        self._videos = []
        self._video_logo = None

        if re.match(r'^https?:/{2}\w.+$', self._video_url):
            self._process_url()
        else:
            raise YoutubeDlError('This url: {0} looks invalid.'.format(self._video_url))

    # 暴露在外在api接口：设置视频名字
    def setVideoName(self, video_name):
        self._filename = video_name
        if self.getVideos():
            for video in self.getVideos():
                video.video_name = video_name
        return True

    # 暴露在外在api接口：获取所有视频的信息
    def getVideos(self):
        return self._videos

    # 暴露在外在api接口：获取视频名字
    def getVideoName(self):
        return self._filename

    # 暴露在外在api接口：筛选想要的视频
    def screeningVideo(self, extension=None, definition=None, profile=None):
        """
        获取已筛选想要的视频列表，并提供文件扩展名和/或
         分辨率和/或质量概况。
        :param extension: 所需的文件扩展名（例如：mp4，flv）。
        :param definition:  所需的视频的清晰度（例如：720p，1080p）
        :param profile: 所需的质量概况（这是主观的，我不推荐
             使用它）。
        :return:
        """
        screening_list = []
        for item in self.getVideos():
            if extension and item.extension != extension:
                continue
            elif definition and item.definition != definition:
                continue
            elif profile and item.profile != profile:
                continue
            else:
                screening_list.append(item)
        return screening_list

    @property
    # 获取原视频的名字，并过滤掉名字中无意义的符号
    # 利用safe_filename（）封装的方法，获得安全名字
    def _video_name(self):
        if not self._filename:
            self._filename = safe_filename(self._title)
        return self._filename

    def _process_url(self):
        """
            解析和处理网址,这一步是创建实例后处理的关键函数；
            其中完成了视频爬取的全部工作。
        """
        # 获取视频详细信息。
        video_data = self._get_video_data()

        # 重写并将该网址添加到javascript文件中，
        # 如果YouTube不提供给我们的签名，我们需要提取这个URL。
        js_partial_url = video_data.get('assets', {}).get('js')
        if js_partial_url.startswith('//'):
            js_url = 'http:' + js_partial_url
        elif js_partial_url.startswith('/'):
            js_url = 'https://youtube.com' + js_partial_url

        # 从标题中设置标题。
        self._title = video_data.get('args', {}).get('title')

        # 创建中间变量，让他们容易作为变量去使用。
        url_encoded_stream = video_data.get('args', {}).get('url_encoded_fmt_stream_map')
        stream_map = self._parse_encode_stream(url_encoded_stream)
        video_urls = stream_map.get('url')

        video_logo = video_data.get('args', {}).get('player_response')
        reg = r'"url":"(.*?)","width"'
        self._video_logo = re.findall(reg, video_logo)[-1]

        # 对于每个视频网址，确定质量配置文件并将其添加到可用视频列表中。
        for i, url in enumerate(video_urls):
            try:
                itag, quality_profile = self._get_quality_profile(url)
                if not quality_profile:
                    log.warn('we cannot identify the video profile for itag=%s', itag)
                    continue
            except(TypeError, KeyError):
                continue

            # 检查我们是否有签名，否则我们需要从js获取密码。
            if 'signature=' not in url:
                signature = self._use_cypher_get_signature(stream_map['s'][i], js_url)
                url = '{0}&signature={1}'.format(url, signature)
            self._add_video(url, self._video_logo, self._video_name, **quality_profile)

        # 清除缓存的js。
        self._js_cache = None

    # 当函数的参数不确定时，可以使用*args 和**kwargs，
    # *args 没有key值，**kwargs有key值。
    def _add_video(self, url, video_logo, video_name, **kwargs):
        """
        实例化一个新视频对象，将所有的视频信息传给实例对象。
        这一步实际上是将url解析出来的信息整合，创建一个类实例，0.1.0版本的
        的功能还局限在下载上，以后会添加其他功能。
        :param url: 视频的签名网址。
        :param video_name: 视频的文件名。
        :param kwargs: 为视频对象设置的附加属性。
        :return:
        """
        _video_instance = Video(url, video_logo,video_name, **kwargs)
        self._videos.append(_video_instance)
        self._videos.sort()
        return True

    # 使用密码获取签名。
    def _use_cypher_get_signature(self, signature, url):
        reg_exp = re.compile(r'"signature",\s?([a-zA-Z0-9$]+)\(')
        # 缓存js，因为`_use_cypher_get_signature()`将被调用为每个视频。
        if not self._js_cache:
            response = urlopen(url)
            if not response:
                raise YoutubeDlError('Unable to open url: {0}'.format(url))
            self._js_cache = response.read().decode()
        try:
            matches = reg_exp.search(self._js_cache)
            if matches:
                # 返回第一个匹配组。
                func = next(g for g in matches.groups() if g is not None)
            # 将js加载到JS Python解释器中。
            jsi = JSInterpreter(self._js_cache)
            initial_function = jsi.extract_function(func)
            return initial_function([signature])
        except Exception as e:
            raise CypherError("Couldn't cipher the signature. Maybe YouTube "
                              'has changed the cipher algorithm. Notify this '
                              'issue on GitHub: {0}'.format(e))
        return False

    # 获取视频网址的质量配置文件。 通常我们会的使用`urlparse`，
    # 因为它表示为一个get参数，但是YouTube没有传递正确编码的网址。
    def _get_quality_profile(self, video_url):
        reg = re.compile('itag=(\d+)')
        itag = reg.findall(video_url)
        if itag and len(itag) == 1:
            itag = int(itag[0])
            # 给定一个itag,
            # 请参阅YouTube质量配置文件以获取视频的属性（媒体类型，分辨率等）。
            quality_frofile = QUALITY_PROFILES.get(itag)
            if not quality_frofile:
                return itag, None
            # 我们将质量配置文件密钥合并到由itag引用的相应质量配置文件中。
            return itag, dict(list(zip(QUALITY_PROFILE_KEYS, quality_frofile)))
        elif not itag:
            raise YoutubeDlError('we cannot find itag to get encoding profile')
        elif len(itag) > 1:
            raise YoutubeDlError('we find multiple itags to get encoding profile, it is wrong')
        return False

    # 获取页面并提取视频数据。
    def _get_video_data(self):

        url_response = urlopen(self._video_url)
        if not url_response:
            raise YoutubeDlError('You cannot open url: {0}'.format(self._video_url))

        html = url_response.read()

        if isinstance(html, str):
            restriction_pattern = 'og:restrictions:age'
        else:
            restriction_pattern = bytes('og:restrictions:age', 'utf-8')

        if restriction_pattern in html:
            raise AgeRestricted('Age restricted video. Unable to download '
                                'without being signed in.')

        # 从html响应体中提取json数据。
        json_object = self._get_json_data(html)

        return json_object

    # 解码YouTube的流文件
    @staticmethod
    def _parse_encode_stream(url_encoded_stream):
        dct = defaultdict(list)
        # 用逗号分隔视频。
        videos = url_encoded_stream.split(',')
        # 取消引用字符，并将其拆分为参数。
        videos = [video.split('&') for video in videos]
        # 在等号上分割，这样我们可以打破这个键值对，并把它折成一个字典。
        for video in videos:
            for kv in video:
                key, value = kv.split('=')
                dct[key].append(unquote(value))
        log.debug('decoded stream: %s', dct)
        return dct

    def _get_json_data(self, html):
        """
        从html中提取json。
        :param html:原始HTML页面。
        :return:
        """
        start_position = self.__json_data_start(html)
        html = html[start_position:]
        end_position = self.__json_data_end(html)
        html = html[:end_position]
        if isinstance(html, str):
            json_data = json.loads(html)
        else:
            json_data = json.loads(html.decode('utf-8'))
        return json_data

    @staticmethod
    def __json_data_start(html):
        if isinstance(html, str):
            start_pattern = 'ytplayer.config = '
        else:
            start_pattern = bytes('ytplayer.config = ', 'utf-8')

        pattern_idx = html.find(start_pattern)
        # 视频无法播放
        if pattern_idx == -1:
            raise YoutubeDlError('we cannot find start pattern')
        # 18表示“ytplayer.config =”的长度。
        start_position = pattern_idx + 18
        return start_position

    @staticmethod
    def __json_data_end(html):
        braces_unmatched_num = 0
        offset = 1
        for i, ch in enumerate(html):
            if isinstance(ch, int):
                ch = chr(ch)
            if ch == '{':
                braces_unmatched_num += 1
            elif ch == '}':
                braces_unmatched_num -= 1
                if braces_unmatched_num == 0:
                    break
        else:
            raise YoutubeDlError('We cannot determine the json offset')
        offset = offset + i
        return offset
