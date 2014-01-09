#!/usr/bin/python

import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

from basehandler import BaseHandler

class TestHandler(BaseHandler):
    def get(self):
        '''Write out to screen
        '''
        self.write("Test of Hello, World");

class PostHandler(BaseHandler):
	def post(self):
		'''Respond with arg1 default input
		'''
		arg1 = self.get_float_arg("arg1",default=1.0);
		self.write_json({"arg1":arg1,"arg2":4*arg1});

	def get(self):
		'''respond with arg1*2
		'''
		arg1 = self.get_float_arg("arg1",default="none");
		self.write("Get from Post Handler " + str(arg1*2));

class FileUploadHandler(BaseHandler):
    def post(self):
        print str(self.request)
        #nginx must be running for this to work properly
        # you will need to forward the fields to get it running
        # something like _name and _path