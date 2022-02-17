# -*- coding: utf-8 -*-
import ssl
import sys
import time
import urllib.error
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

arg = ''
try:
    arg = sys.argv[1]
except IndexError:
    arg = 'error'
path = arg

path = '/Users/lcy/Documents/code/alfred/SHWorkFlow/shlg.py'


def _encode_multipart(params_dict):
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in params_dict.items():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            content = v.read()
            decoded_content = content.decode('UTF-8')
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Type: application/octet-stream\r\n')
            data.append(decoded_content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v if isinstance(v, str) else v.decode('utf-8'))
        data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary


params = {
    'file': open(path, 'rb'),
}
coded_params, boundary = _encode_multipart(params)

url = 'https://c4idl.shinho.net.cn/api/app/version/upload?userKey=063752fe5832'
req = urllib.request.Request(url, coded_params.encode("UTF-8"))
req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
try:
    resp = urllib.request.urlopen(req)
    body = resp.read().decode('utf-8')
    print(body)
except urllib.error.HTTPError as e:
    print(e.fp.read())
