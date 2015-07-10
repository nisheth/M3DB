#utils.py
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
import urllib2
import urllib
import traceback
import json
from M3DB.models import *
from M3api.views import *

def call_api(request, api, params={}, is_post=False):
    if 'projectID' in request.session: params['projectID'] = request.session['projectID']
    try:
        token = Token.objects.get(user=request.user)
        args = urllib.urlencode(params, doseq=True)
        url = handle = None
        if not is_post:
            url = request.build_absolute_uri(reverse(api))+'?%s' % args
            handle = urllib2.Request(url)
        else: 
            url = request.build_absolute_uri(reverse(api))
            handle = urllib2.Request(url, args)
        authheader = "Token %s" % token.key
        handle.add_header("Authorization", authheader)
        results = urllib2.urlopen(handle)
        data = json.load(results)
        return data
    except: raise Exception(traceback.format_exc())