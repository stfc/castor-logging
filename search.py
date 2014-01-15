#!/usr/bin/env python2

from json import load
from urllib2 import urlopen
from prettytable import PrettyTable
from ConfigParser import RawConfigParser
from datetime import datetime
from argparse import ArgumentParser


with open('config.json') as config_file:
    config = load(config_file)

parser = ArgumentParser(description='Search CASTOR logs.')
parser.add_argument('field', type=str, help='')
parser.add_argument('value', type=str, help='')
args = parser.parse_args()

now = datetime.now()
date_info = {
  'year' : now.year,
  'month' : now.month,
  'day' : now.day,
  'hour' : now.hour,
}
del now

url = 'http://%(server)s:%(port)s/%(index)s/_search?q=' % config
url = url % date_info
url += '%(field)s:%%22%(value)s%%22' % vars(args)

results = load(urlopen(url))

fields = [
    u'@timestamp',
    u'syslog_program',
    u'castor_LVL',
    u'castor_MSG',
    u'castor_DiskServer',
]

table = PrettyTable(field_names=fields)

for message in results['hits']['hits']:
    message = message['_source']
    line = []
    for field in fields:
        if field in message:
            line.append(message[field])
        else:
            line.append("")
    table.add_row(line)

print table.get_string(sortby='@timestamp')
