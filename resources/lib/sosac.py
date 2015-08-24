# -*- coding: UTF-8 -*-
# /*
# *      Copyright (C) 2015 Libor Zoubek + jondas
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */

import re
import urllib
import urllib2
import cookielib
import xml.etree.ElementTree as ET
import sys
from bs4 import BeautifulSoup

import util
from provider import ContentProvider, cached, ResolveException

sys.setrecursionlimit(10000)

MOVIES_BASE_URL = "http://movies.prehraj.me"
TV_SHOWS_BASE_URL = "http://tv.prehraj.me"
CHANNEL_SHOWS_action_BASE_URL = "http://tv.prehraj.me/cs/channel/action"
CHANNEL_SHOWS_adventure_BASE_URL = "http://tv.prehraj.me/cs/channel/adventure"
CHANNEL_SHOWS_animation_BASE_URL = "http://tv.prehraj.me/cs/channel/animation"
CHANNEL_SHOWS_biography_BASE_URL = "http://tv.prehraj.me/cs/channel/biography"
CHANNEL_SHOWS_cartoons_BASE_URL = "http://tv.prehraj.me/cs/channel/cartoons"
CHANNEL_SHOWS_comedy_BASE_URL = "http://tv.prehraj.me/cs/channel/comedy"
CHANNEL_SHOWS_crime_BASE_URL = "http://tv.prehraj.me/cs/channel/crime"
CHANNEL_SHOWS_disaster_BASE_URL = "http://tv.prehraj.me/cs/channel/disaster"
CHANNEL_SHOWS_documentary_BASE_URL = "http://tv.prehraj.me/cs/channel/documentary"
CHANNEL_SHOWS_drama_BASE_URL = "http://tv.prehraj.me/cs/channel/drama"
CHANNEL_SHOWS_fairytales_BASE_URL = "http://tv.prehraj.me/cs/channel/fairytales"
CHANNEL_SHOWS_family_BASE_URL = "http://tv.prehraj.me/cs/channel/family"
CHANNEL_SHOWS_fantasy_BASE_URL = "http://tv.prehraj.me/cs/channel/fantasy"
CHANNEL_SHOWS_history_BASE_URL = "http://tv.prehraj.me/cs/channel/history"
CHANNEL_SHOWS_horror_BASE_URL = "http://tv.prehraj.me/cs/channel/horror"
CHANNEL_SHOWS_krimi_BASE_URL = "http://tv.prehraj.me/cs/channel/krimi"
CHANNEL_SHOWS_music_BASE_URL = "http://tv.prehraj.me/cs/channel/music"
CHANNEL_SHOWS_mystery_BASE_URL = "http://tv.prehraj.me/cs/channel/mystery"
CHANNEL_SHOWS_psychological_BASE_URL = "http://tv.prehraj.me/cs/channel/psychological"
CHANNEL_SHOWS_realitytv_BASE_URL = "http://tv.prehraj.me/cs/channel/realitytv"
CHANNEL_SHOWS_romance_BASE_URL = "http://tv.prehraj.me/cs/channel/romance"
CHANNEL_SHOWS_scifi_BASE_URL = "http://tv.prehraj.me/cs/channel/sci-fi"
CHANNEL_SHOWS_sport_BASE_URL = "http://tv.prehraj.me/cs/channel/sport"
CHANNEL_SHOWS_thriller_BASE_URL = "http://tv.prehraj.me/cs/channel/thriller"
CHANNEL_SHOWS_war_BASE_URL = "http://tv.prehraj.me/cs/channel/war"
CHANNEL_SHOWS_western_BASE_URL = "http://tv.prehraj.me/cs/channel/western"
CHANNEL_MOVIES_action_BASE_URL = "http://movies.prehraj.me/cs/channel/action"
CHANNEL_MOVIES_adventure_BASE_URL = "http://movies.prehraj.me/cs/channel/adventure"
CHANNEL_MOVIES_animation_BASE_URL = "http://movies.prehraj.me/cs/channel/animation"
CHANNEL_MOVIES_biography_BASE_URL = "http://movies.prehraj.me/cs/channel/biography"
CHANNEL_MOVIES_comedy_BASE_URL = "http://movies.prehraj.me/cs/channel/comedy"
CHANNEL_MOVIES_crime_BASE_URL = "http://movies.prehraj.me/cs/channel/crime"
CHANNEL_MOVIES_disaster_BASE_URL = "http://movies.prehraj.me/cs/channel/disaster"
CHANNEL_MOVIES_documentary_BASE_URL = "http://movies.prehraj.me/cs/channel/documentary"
CHANNEL_MOVIES_drama_BASE_URL = "http://movies.prehraj.me/cs/channel/drama"
CHANNEL_MOVIES_erotic_BASE_URL = "http://movies.prehraj.me/cs/channel/erotic"
CHANNEL_MOVIES_fairytales_BASE_URL = "http://movies.prehraj.me/cs/channel/fairytales"
CHANNEL_MOVIES_family_BASE_URL = "http://movies.prehraj.me/cs/channel/family"
CHANNEL_MOVIES_fantasy_BASE_URL = "http://movies.prehraj.me/cs/channel/fantasy"
CHANNEL_MOVIES_history_BASE_URL = "http://movies.prehraj.me/cs/channel/history"
CHANNEL_MOVIES_horror_BASE_URL = "http://movies.prehraj.me/cs/channel/horror"
CHANNEL_MOVIES_imax_BASE_URL = "http://movies.prehraj.me/cs/channel/imax"
CHANNEL_MOVIES_krimi_BASE_URL = "http://movies.prehraj.me/cs/channel/krimi"
CHANNEL_MOVIES_music_BASE_URL = "http://movies.prehraj.me/cs/channel/music"
CHANNEL_MOVIES_mystery_BASE_URL = "http://movies.prehraj.me/cs/channel/mystery"
CHANNEL_MOVIES_psychological_BASE_URL = "http://movies.prehraj.me/cs/channel/psychological"
CHANNEL_MOVIES_publicistic_BASE_URL = "http://movies.prehraj.me/cs/channel/publicistic"
CHANNEL_MOVIES_realitytv_BASE_URL = "http://movies.prehraj.me/cs/channel/realitytv"
CHANNEL_MOVIES_romance_BASE_URL = "http://movies.prehraj.me/cs/channel/romance"
CHANNEL_MOVIES_sport_BASE_URL = "http://movies.prehraj.me/cs/channel/sport"
CHANNEL_MOVIES_talkshow_BASE_URL = "http://movies.prehraj.me/cs/channel/talkshow"
CHANNEL_MOVIES_thriller_BASE_URL = "http://movies.prehraj.me/cs/channel/thriller"
CHANNEL_MOVIES_war_BASE_URL = "http://movies.prehraj.me/cs/channel/war"
CHANNEL_MOVIES_western_BASE_URL = "http://movies.prehraj.me/cs/channel/western"
MOVIES_A_TO_Z_TYPE = "movies-a-z"
TV_SHOWS_A_TO_Z_TYPE = "tv-shows-a-z"
TV_SHOW_FLAG = "#tvshow#"
ISO_639_1_CZECH = "cs"
MOST_POPULAR_TYPE = "most-popular"
RECENTLY_ADDED_TYPE = "recently-added"
SEARCH_TYPE = "search"


class SosacContentProvider(ContentProvider):
    ISO_639_1_CZECH = None
    par = None

    def __init__(self, username=None, password=None, filter=None, reverse_eps=False):
        ContentProvider.__init__(self, name='sosac.ph', base_url=MOVIES_BASE_URL, username=username,
                                 password=password, filter=filter)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
        urllib2.install_opener(opener)
        self.reverse_eps = reverse_eps
        if self.lang == ISO_639_1_CZECH:
            self.ISO_639_1_CZECH = ISO_639_1_CZECH + '/'
        else:
            self.ISO_639_1_CZECH = ''

    def capabilities(self):
        return ['resolve', 'categories', 'search']

    def categories(self):
        result = []
        for title, url in [
            ("Movies", MOVIES_BASE_URL),
            ("TV Shows", TV_SHOWS_BASE_URL),
            ("MOVIES - Akcni",  CHANNEL_MOVIES_action_BASE_URL),
            ("MOVIES - Animovane",  CHANNEL_MOVIES_animation_BASE_URL),
            ("MOVIES - Biografie",  CHANNEL_MOVIES_biography_BASE_URL),
            ("MOVIES - Dobrodruzne",  CHANNEL_MOVIES_adventure_BASE_URL),
            ("MOVIES - Dokumentarni",  CHANNEL_MOVIES_documentary_BASE_URL),
            ("MOVIES - Drama",  CHANNEL_MOVIES_drama_BASE_URL),
            ("MOVIES - Eroticke",  CHANNEL_MOVIES_erotic_BASE_URL),
            ("MOVIES - Fantasy",  CHANNEL_MOVIES_fantasy_BASE_URL),
            ("MOVIES - Historicke",  CHANNEL_MOVIES_history_BASE_URL),
            ("MOVIES - Horor",  CHANNEL_MOVIES_horror_BASE_URL),
            ("MOVIES - Hudebni",  CHANNEL_MOVIES_music_BASE_URL),
            ("MOVIES - IMAX",  CHANNEL_MOVIES_imax_BASE_URL),
            ("MOVIES - Katastroficky",  CHANNEL_MOVIES_disaster_BASE_URL),
            ("MOVIES - Komedie",  CHANNEL_MOVIES_comedy_BASE_URL),
            ("MOVIES - Krimi",  CHANNEL_MOVIES_krimi_BASE_URL),
            ("MOVIES - Krimi (Crime)",  CHANNEL_MOVIES_crime_BASE_URL),            
            ("MOVIES - Mysteriozni",  CHANNEL_MOVIES_mystery_BASE_URL),
            ("MOVIES - Pohadky",  CHANNEL_MOVIES_fairytales_BASE_URL),
            ("MOVIES - Psychologicke",  CHANNEL_MOVIES_psychological_BASE_URL),
            ("MOVIES - Publicisticke",  CHANNEL_MOVIES_publicistic_BASE_URL),
            ("MOVIES - Reality-TV",  CHANNEL_MOVIES_realitytv_BASE_URL),
            ("MOVIES - Rodinne",  CHANNEL_MOVIES_family_BASE_URL),
            ("MOVIES - Romanticke",  CHANNEL_MOVIES_romance_BASE_URL),
            ("MOVIES - Sportovni",  CHANNEL_MOVIES_sport_BASE_URL),
            ("MOVIES - Talk-Show",  CHANNEL_MOVIES_talkshow_BASE_URL),
            ("MOVIES - Thriller",  CHANNEL_MOVIES_thriller_BASE_URL),
            ("MOVIES - Valecne",  CHANNEL_MOVIES_war_BASE_URL),
            ("MOVIES - Western",  CHANNEL_MOVIES_western_BASE_URL),
            ("TV Shows - Akcni",  CHANNEL_SHOWS_action_BASE_URL),
            ("TV Shows - Animovane",  CHANNEL_SHOWS_animation_BASE_URL),
            ("TV Shows - Biografie",  CHANNEL_SHOWS_biography_BASE_URL),
            ("TV Shows - Dobrodruzne",  CHANNEL_SHOWS_adventure_BASE_URL),
            ("TV Shows - Dokumentarni",  CHANNEL_SHOWS_documentary_BASE_URL),
            ("TV Shows - Drama",  CHANNEL_SHOWS_drama_BASE_URL),
            ("TV Shows - Fantasy",  CHANNEL_SHOWS_fantasy_BASE_URL),
            ("TV Shows - Historicke",  CHANNEL_SHOWS_history_BASE_URL),
            ("TV Shows - Horor",  CHANNEL_SHOWS_horror_BASE_URL),
            ("TV Shows - Hudebni",  CHANNEL_SHOWS_music_BASE_URL),
            ("TV Shows - Katastroficky",  CHANNEL_SHOWS_disaster_BASE_URL),
            ("TV Shows - Komedie",  CHANNEL_SHOWS_comedy_BASE_URL),
            ("TV Shows - Kreslene",  CHANNEL_SHOWS_cartoons_BASE_URL),
            ("TV Shows - Krimi",  CHANNEL_SHOWS_krimi_BASE_URL),
            ("TV Shows - Krimi (Crime)",  CHANNEL_SHOWS_crime_BASE_URL),            
            ("TV Shows - Mysteriozni",  CHANNEL_SHOWS_mystery_BASE_URL),
            ("TV Shows - Pohadky",  CHANNEL_SHOWS_fairytales_BASE_URL),
            ("TV Shows - Psychologicke",  CHANNEL_SHOWS_psychological_BASE_URL),
            ("TV Shows - Reality-TV",  CHANNEL_SHOWS_realitytv_BASE_URL),
            ("TV Shows - Rodinne",  CHANNEL_SHOWS_family_BASE_URL),
            ("TV Shows - Romanticke",  CHANNEL_SHOWS_romance_BASE_URL),
            ("TV Shows - Sci-Fi",  CHANNEL_SHOWS_scifi_BASE_URL),
            ("TV Shows - Sportovni",  CHANNEL_SHOWS_sport_BASE_URL),
            ("TV Shows - Thriller",  CHANNEL_SHOWS_thriller_BASE_URL),
            ("TV Shows - Valecne",  CHANNEL_SHOWS_war_BASE_URL),
            ("TV Shows - Western",  CHANNEL_SHOWS_western_BASE_URL),
            ("Movies - Most popular",
             MOVIES_BASE_URL + "/" + self.ISO_639_1_CZECH + MOST_POPULAR_TYPE),
            ("TV Shows - Most popular",
             TV_SHOWS_BASE_URL + "/" + self.ISO_639_1_CZECH + MOST_POPULAR_TYPE),
            ("Movies - Recently added",
             MOVIES_BASE_URL + "/" + self.ISO_639_1_CZECH + RECENTLY_ADDED_TYPE),
            ("TV Shows - Recently added",
             TV_SHOWS_BASE_URL + "/" + self.ISO_639_1_CZECH + RECENTLY_ADDED_TYPE)]:
            item = self.dir_item(title=title, url=url)
            if title == 'Movies' or title == 'TV Shows':
                item['menu'] = {"[B][COLOR red]Add all to library[/COLOR][/B]": {
                    'action': 'add-all-to-library', 'title': title}}
            result.append(item)
        return result

    def search(self, keyword):
        return self.list_search('%s/%ssearch?%s' % (MOVIES_BASE_URL, self.ISO_639_1_CZECH,
                                                    urllib.urlencode({'q': keyword})))

    def a_to_z(self, url_type):
        result = []
        for letter in ['0-9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'e', 'h', 'i', 'j', 'k', 'l', 'm',
                       'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            item = self.dir_item(title=letter.upper())
            item['url'] = self.base_url + "/" + self.ISO_639_1_CZECH + url_type + "/" + letter
            result.append(item)
        return result

    def genres_a_to_z(self, url_type):
        result = []
        for letter in ['0-9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'e', 'h', 'i', 'j', 'k', 'l', 'm',
                       'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            item = self.dir_item(title=letter.upper())            
            item['url'] = self.base_url + "/" + letter            
            result.append(item)
        return result            
        
        
    @staticmethod
    def remove_flag_from_url(url, flag):
        return url.replace(flag, "", count=1)

    @staticmethod
    def is_base_url(url):
        if url in [MOVIES_BASE_URL, TV_SHOWS_BASE_URL, 
                  CHANNEL_MOVIES_action_BASE_URL, CHANNEL_MOVIES_animation_BASE_URL, CHANNEL_MOVIES_biography_BASE_URL, CHANNEL_MOVIES_adventure_BASE_URL, CHANNEL_MOVIES_documentary_BASE_URL, CHANNEL_MOVIES_drama_BASE_URL, CHANNEL_MOVIES_erotic_BASE_URL, CHANNEL_MOVIES_fantasy_BASE_URL, CHANNEL_MOVIES_history_BASE_URL, CHANNEL_MOVIES_horror_BASE_URL, CHANNEL_MOVIES_music_BASE_URL, CHANNEL_MOVIES_imax_BASE_URL, CHANNEL_MOVIES_disaster_BASE_URL, CHANNEL_MOVIES_comedy_BASE_URL, CHANNEL_MOVIES_crime_BASE_URL, CHANNEL_MOVIES_krimi_BASE_URL, CHANNEL_MOVIES_mystery_BASE_URL, CHANNEL_MOVIES_fairytales_BASE_URL, CHANNEL_MOVIES_psychological_BASE_URL, CHANNEL_MOVIES_publicistic_BASE_URL, CHANNEL_MOVIES_realitytv_BASE_URL, CHANNEL_MOVIES_family_BASE_URL, CHANNEL_MOVIES_romance_BASE_URL, CHANNEL_MOVIES_sport_BASE_URL, CHANNEL_MOVIES_talkshow_BASE_URL, CHANNEL_MOVIES_thriller_BASE_URL, CHANNEL_MOVIES_war_BASE_URL, CHANNEL_MOVIES_western_BASE_URL,
                  CHANNEL_SHOWS_action_BASE_URL, CHANNEL_SHOWS_animation_BASE_URL, CHANNEL_SHOWS_biography_BASE_URL, CHANNEL_SHOWS_adventure_BASE_URL, CHANNEL_SHOWS_documentary_BASE_URL, CHANNEL_SHOWS_drama_BASE_URL, CHANNEL_SHOWS_fantasy_BASE_URL, CHANNEL_SHOWS_history_BASE_URL, CHANNEL_SHOWS_horror_BASE_URL, CHANNEL_SHOWS_music_BASE_URL, CHANNEL_SHOWS_disaster_BASE_URL, CHANNEL_SHOWS_comedy_BASE_URL, CHANNEL_SHOWS_cartoons_BASE_URL, CHANNEL_SHOWS_crime_BASE_URL, CHANNEL_SHOWS_krimi_BASE_URL, CHANNEL_SHOWS_mystery_BASE_URL, CHANNEL_SHOWS_fairytales_BASE_URL, CHANNEL_SHOWS_psychological_BASE_URL, CHANNEL_SHOWS_realitytv_BASE_URL, CHANNEL_SHOWS_family_BASE_URL, CHANNEL_SHOWS_romance_BASE_URL, CHANNEL_SHOWS_scifi_BASE_URL, CHANNEL_SHOWS_sport_BASE_URL, CHANNEL_SHOWS_thriller_BASE_URL, CHANNEL_SHOWS_war_BASE_URL, CHANNEL_SHOWS_western_BASE_URL
                  ]:
            return True
        else:
            return False

    @staticmethod
    def is_movie_url(url):
        if MOVIES_BASE_URL in url:
            return True
        else:
            return False

    @staticmethod
    def is_tv_shows_url(url):
        if TV_SHOWS_BASE_URL in url:
            return True
        else:
            return False

    @staticmethod
    def is_most_popular(url):
        if MOST_POPULAR_TYPE in url:
            return True
        else:
            return False

    @staticmethod
    def is_recently_added(url):
        if RECENTLY_ADDED_TYPE in url:
            return True
        else:
            return False

    @staticmethod
    def is_search(url):
        return SEARCH_TYPE in url

    @staticmethod
    def particular_letter(url):
        return "a-z" in url

    def has_tv_show_flag(self, url):
        return TV_SHOW_FLAG in url

    def remove_flags(self, url):
        return url.replace(TV_SHOW_FLAG, "", 1)

    def list(self, url):
        print("Examining url", url)
        if self.is_most_popular(url):
            if "movie" in url:
                return self.list_movies_by_letter(url)
            if "tv" in url:
                return self.list_tv_shows_by_letter(url)
                
        if self.is_recently_added(url):
            util.debug("is recently added")
            if "movie" in url:
                return self.list_movie_recently_added(url)
            if "tv" in url:
                util.debug("is TV")
                return self.list_tv_recently_added(url)
                
        if self.is_search(url):
            return self.list_search(url)
            
        if self.is_base_url(url):
            self.base_url = url
            if "channel" in url:
                return self.genres_a_to_z("")                            
            if "movie" in url:
                return self.a_to_z(MOVIES_A_TO_Z_TYPE)
            if "tv" in url:
                return self.a_to_z(TV_SHOWS_A_TO_Z_TYPE)
                
        if "channel" in url:
            if "movie" in url:
                return self.list_movies_by_letter(url)
            if "tv" in url:
                return self.list_tv_shows_by_letter(url)                        

        if self.particular_letter(url):
            if "movie" in url:
                return self.list_movies_by_letter(url)
            if "tv" in url:
                return self.list_tv_shows_by_letter(url)

        if self.has_tv_show_flag(url):
            return self.list_tv_show(self.remove_flags(url))

        return [self.dir_item(title="I failed", url="fail")]

    def list_tv_show(self, url):
        result = []
        page = util.request(url)
        data = util.substr(page, '<div class=\"content\">', '<script')
        for s in re.finditer('<strong.+?</ul>', data, re.IGNORECASE | re.DOTALL):
            serie = s.group(0)
            serie_name = re.search('<strong>([^<]+)', serie).group(1)
            for e in re.finditer('<li.+?</li>', serie, re.IGNORECASE | re.DOTALL):
                episode = e.group(0)
                item = self.video_item()
                ep_name = re.search('<a href=\"#[^<]+<span>(?P<id>[^<]+)</span>(?P<name>[^<]+)',
                                    episode)
                if ep_name:
                    item['title'] = '%s %s %s' % (
                        serie_name, ep_name.group('id'), ep_name.group('name'))
                    item['epname'] = ep_name.group('name')
                    item['ep'] = ep_name
                i = re.search('<div class=\"inner-item[^<]+<img src=\"(?P<img>[^\"]+).+?<a href=\"'
                              '(?P<url>[^\"]+)', episode, re.IGNORECASE | re.DOTALL)
                if i:
                    item['img'] = self._url(i.group('img'))
                    item['url'] = i.group('url')
                if i and ep_name:
                    self._filter(result, item)
        if self.reverse_eps:
            result.reverse()
        return result

    def add_video_flag(self, items):
        flagged_items = []
        for item in items:
            flagged_item = self.video_item()
            flagged_item.update(item)
            flagged_items.append(flagged_item)
        return flagged_items

    def add_directory_flag(self, items):
        flagged_items = []
        for item in items:
            flagged_item = self.dir_item()
            flagged_item.update(item)
            flagged_items.append(flagged_item)
        return flagged_items

    @cached(ttl=24)
    def get_data_cached(self, url):
        return util.request(url)

    def list_by_letter(self, url):
        result = []
        page = self.get_data_cached(url)
        data = util.substr(page, '<ul class=\"content', '</ul>')
        subs = self.get_subs()
        for m in re.finditer('<a class=\"title\" href=\"(?P<url>[^\"]+)[^>]+>(?P<name>[^<]+)', data,
                             re.IGNORECASE | re.DOTALL):
            item = {'url': m.group('url'), 'title': m.group('name')}
            if item['url'] in subs:
                item['menu'] = {"[B][COLOR red]Remove from subscription[/COLOR][/B]": {
                    'url': m.group('url'), 'action': 'remove-subscription', 'name': m.group('name')}
                }
            else:
                item['menu'] = {"[B][COLOR red]Add to library[/COLOR][/B]": {
                    'url': m.group('url'), 'action': 'add-to-library', 'name': m.group('name')}}
            self._filter(result, item)
        paging = util.substr(page, '<div class=\"pagination\"', '</div')
        next = re.search('<li class=\"next[^<]+<a href=\"\?page=(?P<page>\d+)', paging,
                         re.IGNORECASE | re.DOTALL)
        if next:
            next_page = int(next.group('page'))
            current = re.search('\?page=(?P<page>\d)', url)
            current_page = 0
            if self.is_most_popular(url) and next_page > 10:
                return result
            if current:
                current_page = int(current.group('page'))
            if current_page < next_page:
                url = re.sub('\?.+?$', '', url) + '?page=' + str(next_page)
                result += self.list_by_letter(url)
        return result

    def list_tv_recently_added(self, url):
        result = []
        page = self.get_data_cached(url)
        data = util.substr(page, '<div class=\"content\"', '</ul>')
        subs = self.get_subs()
        for m in re.finditer('<a href=\"(?P<url>[^\"]+)[^>]+((?!<strong).)*<strong>S(?P<serie>\d+) '
                             '/ E(?P<epizoda>\d+)</strong>((?!<a href).)*<a href=\"(?P<surl>[^\"]+)'
                             '[^>]+class=\"mini\">((?!<span>).)*<span>\((?P<name>[^)]+)\)<',
                             data, re.IGNORECASE | re.DOTALL):
            item = self.video_item()
            item['url'] = m.group('url')
            item['title'] = "Rada " + m.group('serie') + " Epizoda " + m.group(
                'epizoda') + " - " + m.group('name')
            if item['url'] in subs:
                item['menu'] = {"[B][COLOR red]Remove from subscription[/COLOR][/B]": {
                    'url': m.group('url'), 'action': 'remove-subscription',
                    'name': m.group('name') + " S" + m.group('serie') + 'E' + m.group('epizoda')}}
            else:
                item['menu'] = {"[B][COLOR red]Add to library[/COLOR][/B]": {
                    'url': m.group('url'), 'action': 'add-to-library',
                    'name': m.group('name') + " S" + m.group('serie') + 'E' + m.group('epizoda')}}
            self._filter(result, item)
        paging = util.substr(page, '<div class=\"pagination\"', '</div')
        next = re.search('<li class=\"next[^<]+<a href=\"\?page_1=(?P<page>\d+)', paging,
                         re.IGNORECASE | re.DOTALL)
        if next:
            next_page = int(next.group('page'))
            current = re.search('\?page_1=(?P<page>\d)', url)
            current_page = 0
            if next_page > 30:
                return result
            if current:
                current_page = int(current.group('page'))
            if current_page < next_page:
                url = re.sub('\?.+?$', '', url) + '?page_1=' + str(next_page)
                result += self.list_tv_recently_added(url)
        return result

    def library_movie_recently_added_xml(self):
        data = util.request(
            'http://tv.prehraj.me/filmyxml2.php?limit=10000&sirka=670&vyska=377&affid=0#')
        tree = ET.fromstring(data)
        total = float(len(list(tree.findall('film'))))
        print("TOTAL: ", total)
        num = 0
        for film in tree.findall('film'):
            num += 1
            perc = float(num / total) * 100
            print("percento: ", int(perc))
            if self.parent.dialog.iscanceled():
                return
            self.parent.dialog.update(int(perc), film.findtext('nazeven'))
            item = self.video_item()
            try:
                item['title'] = '%s (%s)' % (
                    film.findtext('nazeven').encode('utf-8'), film.findtext('rokvydani'))
                item['name'] = item['title'].encode('utf-8')
                item['url'] = 'http://movies.prehraj.me/player/' + self.parent.make_name(
                    film.findtext('nazeven').encode('utf-8') + '-' + film.findtext('rokvydani'))
                item['menu'] = {"[B][COLOR red]Add to library[/COLOR][/B]": {
                    'url': item['url'], 'action': 'add-to-library', 'name': item['title']}}
                item['update'] = True
                item['notify'] = False
                self.parent.add_item(item)
                # print("TITLE: ", item['title'])
            except Exception, e:
                print("ERR TITLE: ", item['title'], e)
                pass
        self.parent.dialog.close()

    def library_tvshows_all_xml(self):
        page = util.request('http://tv.prehraj.me/serialyxml.php')
        data = util.substr(page, '<select name=\"serialy\">', '</select>')
        items = re.finditer('<option value=\"(?P<url>[^\"]+)\">(?P<name>[^<]+)</option>', data,
                            re.IGNORECASE | re.DOTALL)
        total = float(len(list(items)))
        items = re.finditer('<option value=\"(?P<url>[^\"]+)\">(?P<name>[^<]+)</option>', data,
                            re.IGNORECASE | re.DOTALL)
        print("Pocet: ", total)
        num = 0
        for m in items:
            num += 1
            if self.parent.dialog.iscanceled():
                return
            perc = float(num / total) * 100
            print("percento: ", int(perc))
            self.parent.dialog.update(int(perc), m.group('name'))
            item = {'url': 'http://tv.prehraj.me/cs/detail/' + m.group('url'),
                    'action': 'add-to-library', 'name': m.group('name'), 'update': True,
                    'notify': True}
            self.parent.add_item(item)

        print("done....")

    def list_movie_recently_added(self, url):
        result = []
        page = self.get_data_cached(url)
        data = util.substr(page, '<div class=\"content\"', '</ul>')
        for m in re.finditer(
                '<a class=\"content-block\" href=\"(?P<url>[^\"]+)\" title=\"(?P<name>[^\"]+)',
                data, re.IGNORECASE | re.DOTALL):
            item = self.video_item()
            item['url'] = m.group('url')
            item['title'] = m.group('name')
            item['menu'] = {"[B][COLOR red]Add to library[/COLOR][/B]": {
                'url': m.group('url'), 'action': 'add-to-library', 'name': m.group('name')}}
            self._filter(result, item)
        paging = util.substr(page, '<div class=\"pagination\"', '</div')
        next = re.search('<li class=\"next[^<]+<a href=\"\?page=(?P<page>\d+)', paging,
                         re.IGNORECASE | re.DOTALL)
        if next:
            next_page = int(next.group('page'))
            current = re.search('\?page=(?P<page>\d)', url)
            current_page = 0
            if next_page > 5:
                return result
            if current:
                current_page = int(current.group('page'))
            if current_page < next_page:
                url = re.sub('\?.+?$', '', url) + '?page=' + str(next_page)
                result += self.list_movie_recently_added(url)
        return result

    def add_flag_to_url(self, item, flag):
        item['url'] = flag + item['url']
        return item

    def add_url_flag_to_items(self, items, flag):
        subs = self.get_subs()
        for item in items:
            if item['url'] in subs:
                item['title'] = '[B][COLOR yellow]*[/COLOR][/B]' + item['title']
            self.add_flag_to_url(item, flag)
        return items

    def _url(self, url):
        return self.base_url + "/" + url.lstrip('./')

    def list_tv_shows_by_letter(self, url):
        print("Getting shows by letter", url)
        shows = self.list_by_letter(url)
        print("Resloved shows", shows)
        shows = self.add_directory_flag(shows)
        return self.add_url_flag_to_items(shows, TV_SHOW_FLAG)

    def list_movies_by_letter(self, url):
        movies = self.list_by_letter(url)
        print("Resolved movies", movies)
        return self.add_video_flag(movies)

    def resolve(self, item, captcha_cb=None, select_cb=None):
        page = util.request(item['url'])
        data = util.substr(page, '<div class=\"bottom-player\"', 'div>')
        if data.find('<iframe') < 0:
            raise ResolveException('Video is not available.')
        result = self.findstreams(data, ['<iframe src=\"(?P<url>[^\"]+)'])
        if len(result) == 1:
            return result[0]
        elif len(result) > 1 and select_cb:
            return select_cb(result)

    def get_subs(self):
        return self.parent.get_subs()

    @staticmethod
    def parse_html(url):
        return BeautifulSoup(util.request(url))

    def list_search(self, url):
        result = []
        html_tree = self.parse_html(url)
        for entry in html_tree.select('ul.content li'):
            item = self.video_item()
            entry.p.strong.extract()
            item['url'] = entry.h4.a.get('href')
            item['title'] = entry.h4.a.text
            item['img'] = MOVIES_BASE_URL + entry.img.get('src')
            item['plot'] = entry.p.text.strip()
            item['menu'] = {"[B][COLOR red]Add to library[/COLOR][/B]": {
                'url': item['url'], 'action': 'add-to-library', 'name': item['title']}}
            self._filter(result, item)
        # Process next 4 pages, so we'll get 20 items per page instead of 4
        for next_page in html_tree.select('.pagination ul li.next a'):
            next_url = '%s/%ssearch%s' % (MOVIES_BASE_URL, self.ISO_639_1_CZECH,
                                          next_page.get('href'))
            page_number = 1
            page = re.search(r'\bpage=(\d+)', url)
            if page:
                page_number = int(page.group(1))
            next_page_number = 1
            page = re.search(r'\bpage=(\d+)', next_url)
            if page:
                next_page_number = int(page.group(1))
            if page_number > next_page_number:
                break
            if page_number % 5 != 0:
                result += self.list_search(next_url)
            else:
                item = self.dir_item()
                item['type'] = 'next'
                item['url'] = next_url
                result.append(item)
            break
        return result
