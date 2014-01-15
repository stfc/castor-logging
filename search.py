#!/usr/bin/env python2
#
#  Copyright 2014 Science & Technology Facilities Council
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

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

fields = config['fields']

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
