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
pages = [
    { "name": "Home",
      "link": "/", 
      "content_file": "contents/home.md"
    },
    { "name": "Info",
      "link": "/info.html", 
      "content_file": "contents/info.md"
    },
    ]
 
# this is the directory with static files (images, css, ...)
static_dir = "public"
 
# the view, layout.html is a template file
htmlview = web.template.render('views', cache=False, base="layout",\
   globals={'pages':pages, 'ctx': web.ctx})
 
# generic controller for Markdown pages:
class PageClassTemplate:
    content_file = ""
 
    def GET(self):
        html = markdown2.markdown_path(self.content_file)
        return htmlview.page(html)
 
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
 
for page in pages:
    pattern = page["link"]
    globals()[page["name"]] = type(page["name"],\
   (PageClassTemplate,object,), dict(content_file=page["content_file"]))
    myApp.add_mapping(pattern, page["name"])
 
# add static file handler:
try:
    if static_dir:
        myApp.add_mapping("/%s/.+" % static_dir, "Public")
except AttributeError:
    pass
 
# RUN!
if __name__ == "__main__":
    myApp.run()
