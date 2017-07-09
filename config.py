#!/usr/bin/env python3
import yaml

data = yaml.safe_load(open('config.yml', 'r'))

def section(section):
    return data[section]

def sections():
    return list(data.keys())
