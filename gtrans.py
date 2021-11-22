# -*- coding: utf-8 -*-
import json
import sys
import os

from googletrans import Translator


sys.path.append(os.path.dirname(os.path.realpath(__file__)))

src = sys.argv[1]

translator = Translator()
result = translator.detect(src)
if result.lang == 'en':
    result = translator.translate(src, dest='zh-CN')
else:
    result = translator.translate(src)

items = {"items": [
    {"title": "翻译结果", "subtitle": result.text, "valid": "true", "arg": result.text}
]}

print(json.dumps(items))
