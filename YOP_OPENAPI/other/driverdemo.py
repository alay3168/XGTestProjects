#! /usr/bin/python
# -*- coding: utf-8 -*-
  
from urllib import quote, urlencode
import urllib2
import time
import uuid
import hmac, hashlib
  
  def get_info(token, secret):
      URI = 'http://api.t.sina.com.cn/account/verify_credentials.json'
      APP_KEY = '' #写自己的
      APP_SECRET = ''
  
      headers = [
          ('oauth_consumer_key', APP_KEY),
          ('oauth_nonce', uuid.uuid4().hex),
          ('oauth_signature_method', 'HMAC-SHA1'),
          ('oauth_timestamp', int(time.time())),
          ('oauth_version', '1.0'),
          ('oauth_token', token)
      ]
  
      headers.sort()
  
      p = 'POST&%s&%s' % (quote(URI, safe=''), quote(urlencode(headers)))
      signature = hmac.new(APP_SECRET + '&' + secret, p,
                           hashlib.sha1).digest().encode('base64').rstrip()
  
      headers.append(('oauth_signature', quote(signature)))
  
      h = ', '.join(['%s="%s"' % (k, v) for (k, v) in headers])
  
      r = urllib2.Request(URI, data='', headers={'Authorization': 'OAuth realm="", %s' % h})
  
      data = urllib2.urlopen(r).read()
      return data
  
  if __name__ == '__main__':
      print get_info('97de3e2422c2b5fe4328d6cdc1ac5597', '2563a0ac36baecbbb7d93a4987d899df')
