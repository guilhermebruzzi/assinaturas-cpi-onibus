#!/usr/bin/env python
#-*- coding:utf-8 -*-

from helpers import get_json

def get_facebook_data(oauth_token):
    me = get_json("https://graph.facebook.com/me?access_token=%s" % oauth_token)
    return me
