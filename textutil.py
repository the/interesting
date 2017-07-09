#!/usr/bin/env python3
import re

def normalized_text(text):
    text = text.replace('\n', ' ')
    text = re.sub('http(s)?://[^ ]+', '', text)
    text = re.sub('  +', ' ', text)
    text = re.sub('[¶]', '', text)
    return text.strip()
