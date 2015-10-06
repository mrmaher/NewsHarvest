from utilities import *
import time

__author__ = 'donnalley'


# todo: implement 'espanol'
# todo: implement dedupe
class AssociatedPress(object):
    def __init__(self, source='home'):
        self.source = source
        self.valid_sources = ['home', 'headlines', 'business', 'us', 'world', 'sports', 'entertainment', 'health',
                              'science', 'politics', 'espanol']
        self.verify_source()
        self.url = 'http://hosted.ap.org/dynamic/fronts/' + source.upper() + '?SITE=AP&SECTION=HOME'
        # NOTE: 'home' and 'headlines' is the only one that is different
        if source == 'home' or source == 'headlines':
            self.container_tag = 'div'
            self.container_attrs = {'class': 'ap-newsbriefitem'}
            self.headline_tag = 'span'
            self.headline_attrs = {'class': 'topheadline'}
            self.excerpt_tag = 'span'
            self.excerpt_attrs = {'class': 'topheadlinebody'}
        elif source == 'business':
            self.container_tag = 'p'
            self.container_attrs = {'class': 'ap-topheadlineitem-p'}
            self.headline_tag = 'span'
            self.headline_attrs = {'class': 'topheadline'}
            self.excerpt_tag = 'span'
            self.excerpt_attrs = {'class': 'topheadlinebody'}
        elif source == 'us':
            self.container_tag = 'p'
            self.container_attrs = {'class': 'ap-topheadlineitem-p'}
            self.headline_tag = 'span'
            self.headline_attrs = {'class': 'topheadline'}
            self.excerpt_tag = 'span'
            self.excerpt_attrs = {'class': 'topheadlinebody'}
        elif source == 'world':
            self.container_tag = 'p'
            self.container_attrs = {'class': 'ap-topheadlineitem-p'}
            self.headline_tag = 'span'
            self.headline_attrs = {'class': 'topheadline'}
            self.excerpt_tag = 'span'
            self.excerpt_attrs = {'class': 'topheadlinebody'}
        elif source == 'sports':
            self.container_tag = 'p'
            self.container_attrs = {'class': 'ap-topheadlineitem-p'}
            self.headline_tag = 'span'
            self.headline_attrs = {'class': 'topheadline'}
            self.excerpt_tag = 'span'
            self.excerpt_attrs = {'class': 'topheadlinebody'}
        elif source == 'entertainment':
            self.container_tag = 'p'
            self.container_attrs = {'class': 'ap-topheadlineitem-p'}
            self.headline_tag = 'span'
            self.headline_attrs = {'class': 'topheadline'}
            self.excerpt_tag = 'span'
            self.excerpt_attrs = {'class': 'topheadlinebody'}
        elif source == 'health':
            self.container_tag = 'p'
            self.container_attrs = {'class': 'ap-topheadlineitem-p'}
            self.headline_tag = 'span'
            self.headline_attrs = {'class': 'topheadline'}
            self.excerpt_tag = 'span'
            self.excerpt_attrs = {'class': 'topheadlinebody'}
        elif source == 'science':
            self.container_tag = 'p'
            self.container_attrs = {'class': 'ap-topheadlineitem-p'}
            self.headline_tag = 'span'
            self.headline_attrs = {'class': 'topheadline'}
            self.excerpt_tag = 'span'
            self.excerpt_attrs = {'class': 'topheadlinebody'}
        elif source == 'politics':
            self.container_tag = 'p'
            self.container_attrs = {'class': 'ap-topheadlineitem-p'}
            self.headline_tag = 'span'
            self.headline_attrs = {'class': 'topheadline'}
            self.excerpt_tag = 'span'
            self.excerpt_attrs = {'class': 'topheadlinebody'}
        # elif source == 'espanol':
        #     self.url = 'http://hosted.ap.org/dynamic/fronts/' + 'NOTICIAS_GENERALES' + '?SITE=AP&SECTION=HOME'
        #     self.container_tag = 'p'
        #     self.container_attrs = {'class': 'ap-topheadlineitem-p'}
        #     self.headline_tag = 'span'
        #     self.headline_attrs = {'class': 'topheadline'}
        #     self.excerpt_tag = 'span'
        #     self.excerpt_attrs = {'class': 'topheadlinebody'}
        else:
            raise AttributeError("Invalid source")

    def verify_source(self):
        if self.source not in self.valid_sources:
            raise AttributeError(
                '''Invalid source. You may only input these sources:
                home, headlines, business, us, world, sports, entertainment, health, science, politics, espanol''')

    def get_data(self, get_content=True, sleep=True, json_format=False, include_headings=False, duplicates=False):
        source = 'Associated Press - ' + self.source
        soup = open_and_soupify_url(self.url)
        output = []
        if include_headings is True and json_format is False:
            headings = ['Source', 'Headline', 'URL', 'Excerpt', 'Location', 'Time', 'Date', 'Content']
            output.append(headings)

        containers = soup.find_all(self.container_tag, attrs=self.container_attrs)
        for container in containers:
            if sleep:
                time.sleep(1)
            headline_and_url = container.find(self.headline_tag, attrs=self.headline_attrs)
            headline = headline_and_url.a.text.strip()
            prefix = 'http://hosted.ap.org/'
            url = prefix + headline_and_url.a['href']
            # skip if duplicate
            if duplicates and url in duplicates:
                continue
            excerpt = container.find(self.excerpt_tag, attrs=self.excerpt_attrs).text.strip()
            try:
                location = parse_location(excerpt)
            except AttributeError:
                location = ''
            date_time = url[-19:]
            date = date_time[:10]
            date = standardize_date(date)
            publish_time = date_time[11:].replace('-', ':')
            if get_content:
                page_content = self.collect_ap_content(url)
            else:
                page_content = ''

            data_point = [source, headline, url, excerpt, location, publish_time, date, page_content]
            output.append(data_point)

        if json_format:
            return transform_to_json(output)
        else:
            return output

    @staticmethod
    def collect_ap_content(url):
        soup = open_and_soupify_url(url)
        content = soup.find_all('p', attrs={'class': 'ap-story-p'})
        output = ''
        for item in content:
            output += item.text
        return output


class Reuters(object):
    def __init__(self, source='businessNews'):
        self.source = source
        self.valid_sources = ['businessNews', 'wealth', 'bankruptcyNews', 'bondsNews', 'deals', 'economy',
                              'globalmarketsNews', 'hedgefunds', 'hotStocksNews', 'mergersNews',
                              'governmentfilingsNews', 'summitNews', 'USdollarreportNews', 'usmarkets']
        self.verify_source()
        self.url = self.get_url()

    def verify_source(self):
        if self.source not in self.valid_sources:
            raise AttributeError(
                '''Invalid source. You may only input these sources:
                businessNews, wealth, bankruptcyNews, bondsNews, deals, economy, globalmarketsNews, hedgefunds,
                hotStocksNews, mergersNews, governmentfilingsNews, summitNews, USdollarreportNews, usmarkets''')

    def get_url(self):
        prefix = 'http://feeds.reuters.com/'
        if self.source in ['wealth', 'deals', 'economy', 'hedgefunds', 'usmarkets']:
            prefix += 'news/'
        else:
            prefix += 'reuters/'
        url = prefix + self.source
        return url

    def get_data(self, get_content=True, sleep=True, include_headings=False, json_format=False, duplicates=False):
        source = 'Reuters - ' + self.source
        soup = open_and_soupify_url(self.url, parser='html.parser')
        output = []
        if include_headings is True and json_format is False:
            headings = ['Source', 'Headline', 'URL', 'Excerpt', 'Location', 'Time', 'Date', 'Content']
            output.append(headings)

        containers = soup.find_all('item')
        for container in containers:
            if sleep:
                time.sleep(1)
            headline = container.find('title').text
            url = container.find('link').text
            # skip if duplicate
            if duplicates and url in duplicates:
                continue
            raw_excerpt = container.find('description').text
            excerpt = clean_html(raw_excerpt)
            try:
                location = parse_location(excerpt)
            except AttributeError:
                location = ''
            pubdate = container.find('pubdate').text
            if pubdate[-13].isdigit():
                date = pubdate[:-14]
                date = standardize_date(date)
                publish_time = pubdate[-13:]
            else:
                date = pubdate[:-13]
                date = standardize_date(date)
                publish_time = pubdate[-12:]
            if get_content:
                page_content = self.get_reuters_content(url)
            else:
                page_content = ''
            data_point = [source, headline, url, excerpt, location, publish_time, date, page_content]
            output.append(data_point)

        if json_format:
            return transform_to_json(output)
        else:
            return output

    @staticmethod
    def get_reuters_content(url):
        soup = open_and_soupify_url(url)
        article = soup.find('span', attrs={'id': 'articleText'})
        content = article.find_all('p')
        output = ''
        for item in content:
            output += item.text
        return output


class Bloomberg(object):
    def __init__(self, source='top news'):
        self.source = source
        if source == 'top news':
            self.homepage = 'http://www.bloomberg.com/'
            self.container_tag = 'li'
            self.container_attrs = {'class': 'top-news-v3__story-view'}
            self.headline_tag = 'h1'
            self.headline_attrs = {'class': 'top-news-v3__story__headline'}
            self.excerpt_tag = 'div'
            self.excerpt_attrs = {'class': 'top-news-v3__story__summary'}
            self.time_tag = 'time'
            self.time_attrs = {'class': 'published-at'}
        elif source == 'markets':
            self.homepage = 'http://www.bloomberg.com/markets/'
            self.container_tag = 'article'
            self.container_attrs = {'class': 'markets-hero__news-reel__story type-article site-bbiz'}
            self.headline_tag = 'h1'
            self.headline_attrs = {'class': 'markets-hero__news-reel__story-headline'}
            self.time_tag = 'time'
            self.time_attrs = {'class': 'published-at'}
        else:
            raise AttributeError('Invalid source. Use top news or markerts')

    def get_data(self, get_content=True, sleep=True, json_format=False, include_headings=False, duplicates=False):
        source = 'Bloomberg - ' + self.source
        soup = open_and_soupify_url(self.homepage, parser='html.parser')
        output = []
        if include_headings is True and json_format is False:
            headings = ['Source', 'Headline', 'URL', 'Excerpt', 'Location', 'Time', 'Date', 'Content']
            output.append(headings)

        containers = soup.find_all(self.container_tag, attrs=self.container_attrs)
        for container in containers:
            if sleep:
                time.sleep(1)
            headline = container.find(self.headline_tag, attrs=self.headline_attrs).text.strip()\
                .encode('ascii', errors='ignore')
            url = container.find(self.headline_tag, attrs=self.headline_attrs).a['href']
            if self.homepage not in url:
                url = self.homepage.replace('markets/', '') + url
            # skip if duplicate
            if duplicates and url in duplicates:
                continue
            if self.source == 'top news':
                try:
                    excerpt = container.find(self.excerpt_tag, attrs=self.excerpt_attrs).text.strip()
                except AttributeError:
                    excerpt = ''
            else:
                excerpt = ''
            location = ''
            try:
                date_time = container.find(self.time_tag, attrs=self.time_attrs)['datetime']
                date = date_time[:10]
                date = standardize_date(date)
                regex = re.compile('T(.*)$')
                publish_time = regex.search(date_time).group(1)[:-2]
            except TypeError:
                date = ''
                publish_time = ''
            if get_content:
                page_content = self.get_bloomberg_content(url)
            else:
                page_content = ''
            data_point = [source, headline, url, excerpt, location, publish_time, date, page_content]
            output.append(data_point)

        if json_format:
            return transform_to_json(output)
        else:
            return output

    @staticmethod
    def get_bloomberg_content(url):
        soup = open_and_soupify_url(url)
        content = soup.find_all('p')
        output = ''
        for item in content:
            output += item.text.encode('ascii', errors='ignore')
        print output
        return output


# DEPRECATED
class GoogleFinance(object):
    def __init__(self):
        self.url = 'https://www.google.com/finance/market_news'

    def get_data(self, get_content=True, sleep=True):
        soup = open_and_soupify_url(self.url, parser='html.parser')
        output = []
        # headings = ['Headline', 'URL', 'Excerpt', 'Location', 'Time', 'Date', 'Content']
        # output.append(headings)

        containers = soup.find_all('div', attrs={'class': 'g-section news sfe-break-bottom-16'})
        for container in containers:
            if sleep:
                time.sleep(1)
            headline = container.find('span', attrs={'class': 'name'}).text.strip()
            print headline
            url = container.find('span', attrs={'class': 'name'}).a['href']
            print url
            excerpt = container.find('div', attrs={'style': 'width:100%;'}).text
            print excerpt
            location = ''
            publish_time = ''
            date = ''
            if get_content:
                page_content = collect_content(url)
            else:
                page_content = ''
            data_point = [headline, url, excerpt, location, publish_time, date, page_content]
            output.append(data_point)
