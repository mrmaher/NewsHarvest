import json
import csv
from bs4 import BeautifulSoup
import requests
import re
import collections
import datetime

__author__ = 'donnalley'


# I/O Functions #####################################################
def open_json(input_file):
    with open(input_file, 'r') as infile:
        input_data = json.load(infile)
    return input_data


def write_json(data, output_file):
    try:
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=True)
    except IOError as (error_number, strerror):
        print("I/O error({0}): {1}".format(error_number, strerror))
    return


def write_to_txt(data, output_file):
    try:
        with open(output_file, 'w') as outfile:
            for line in data:
                outfile.write(line + '\n')
    except IOError as (error_number, strerror):
        print("I/O error({0}): {1}".format(error_number, strerror))
    return


def write_to_csv(data, output_file):
    try:
        with open(output_file, 'wb') as myCSVFile:
            csv_writer = csv.writer(myCSVFile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            for data in data:
                csv_writer.writerow(map(encode, data))
    except IOError as (error_number, strerror):
        print("I/O error({0}): {1}".format(error_number, strerror))
    return


def append_to_csv(data, output_file):
    try:
        with open(output_file, 'ab') as myCSVFile:
            csv_writer = csv.writer(myCSVFile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            for data in data:
                csv_writer.writerow(map(encode, data))
    except IOError as (error_number, strerror):
        print("I/O error({0}): {1}".format(error_number, strerror))
    return


# HELPER FUNCTIONS ###################################################
def encode(item):
    return item.encode('ascii', errors='ignore')


def transform_to_json(list_data):
    output = collections.OrderedDict()
    output['source'] = list_data[0][0]
    stories = []
    for item in list_data:
        data_point = collections.OrderedDict()
        data_point['headline'] = item[1]
        data_point['url'] = item[2]
        data_point['excerpt'] = item[3]
        data_point['location'] = item[4]
        data_point['publish_time'] = item[5]
        data_point['date'] = item[6]
        data_point['page_content'] = item[7]
        stories.append(data_point)
    output['stories'] = stories
    return output


def open_and_soupify_url(url, parser='html.parser'):
    headers = {'user-agent': 'Mozilla/5.0'}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, parser)
    return soup


def get_month():
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar',
              4: 'Apr', 5: 'May', 6: 'Jun',
              7: 'Jul', 8: 'Aug', 9: 'Sep',
              10: 'Oct', 11: 'Nov', 12: 'Dec'}
    month = datetime.date.today().month
    return months[month]


def parse_location(text):
    try:
        if '*' in text[0]:
            location = ''
            return location
    except IndexError:
        location = ''
        return location
    regex = re.compile("(.*?)\s*\(")
    location = regex.match(text).group(1)
    month = get_month()
    if month in location:
        raw_regex = r"(.*?)\s*,\s" + month
        regex = re.compile(raw_regex)
        location = regex.match(location).group(1)
    return location


def standardize_date(date_string):
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3,
              'Apr': 4, 'May': 5, 'Jun': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9,
              'Oct': 10, 'Nov': 11, 'Dec': 12}
    days = ['Mon', 'Tue', 'Wed', 'Thur', 'Thu', 'Fri', 'Sat', 'Sun']
    if date_string[:3] in days:
        date_string = date_string[5:]
        pieces = date_string.split()
        day = pieces[0]
        month = str(months[pieces[1]])
        year = pieces[2]
        date_string = month + "/" + day + "/" + year
    return date_string


# Deprecated
def collect_content(link):
    if '.pdf' in link:
        content = 'Error: PDF'
    else:
        try:
            html = requests.get(link, headers={'user-agent': 'Mozilla/5.0'}).text
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.find_all(text=True)
            content = filter(visible, text)
            content = ' '.join(content).encode('ascii', errors='ignore')
            content = content.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
            content = clean_html(content)
        except (requests.HTTPError, requests.exceptions.ConnectionError, ValueError):
            content = 'Error: 404 not found'
    return content


def clean_html(html_text):
    # Remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(<!--\1-->)", "", html_text.strip())
    # Remove html comments. This has to be done before removing regular tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # deal with whitespace
    cleaned = re.sub(r" ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('ascii', errors='ignore'))):
        return False
    elif re.match('\n', str(element.encode('ascii', errors='ignore'))):
        return False
    return True
