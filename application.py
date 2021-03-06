#!/usr/bin/python26
# vi:si:et:sw=4:sts=4:ts=4
# -*- coding: UTF-8 -*-
# -*- Mode: Python -*-
#
# Copyright (C) 2011 Bertera Pietro

import web
import mimetypes

import markdown2

# pages is a list of dictionary: the value of key name represent the name\
# of page, the value of link represent the routing pattern,
# and content_file is the path of markdown file with the page content
pages = []
 
# this is the directory with static files (images, css, ...)
static_dir = "public"
 
# the view, layout.html is a template file
htmlview = web.template.render('views', cache=False, base="layout",\
   globals={'pages':pages, 'ctx': web.ctx})
 
 
# Controller for static files
class Public:
    def GET(self):
        try:
            file_name = web.ctx.path.split('/')[-1]
            web.header('Content-type', mime_type(file_name))
            return open('.' + web.ctx.path, 'rb').read()
        except IOError:
            raise web.notfound()
 
# mime type interpreter
def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
 
# initialize the application
myApp = web.application(mapping=(), fvars=globals())
myApp.add_mapping('/refesh', 'Refesh')
myApp.add_mapping('/([^\.]*)', 'Controller')

class Controller:
    def GET(self,key):
        html = markdown2.markdown_path("contents/"+key+'.md')
        return htmlview.page(html)

class Refesh:
    def GET(self):
        import os
        dir=  'contents'
        files = os.listdir(dir) 
        global pages 
        for f in files:  
            pages.append(f.replace('.md',''))
        print pages
        return 'success'
 
# add static file handler:
try:
    if static_dir:
        myApp.add_mapping("/%s/.+" % static_dir, "Public")
except AttributeError:
    pass
 
# RUN!
if __name__ == "__main__":
    myApp.run()
