#!/usr/bin/python

import tornado.ioloop
import tornado.web
import tornado.httpclient

import pdb

with open('../flickr.txt') as fid:
    flickr_search = fid.read()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, MSLC World")

class GetExampleHandler(tornado.web.RequestHandler):
    def get(self):
        print("received get request")
        arg = self.get_argument("arg", None, True) # get the argument
        if arg is None:
            self.write("No 'arg' in query")
        else:
            self.write(str(arg)) # spit back out the argument

class SearchHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write("Searching on Flickr...")
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = http_client.fetch(flickr_search,
            callback=self.handle_response)  # call when finished      

    def handle_response(self,response):
        #strip make valid representation for json
        body = str(response.body.decode('UTF-8')).replace("</", "<\\/")

        self.set_header("Content-Type", "application/json") # display as json in webpage
        # write the response
        self.write(" and we got a response! \n") 
        self.write(body) 

        self.finish() # and finish the request off
        

handlers = [(r"/", MainHandler),
            (r"/GetExample", GetExampleHandler),
            (r"/Flickr",SearchHandler),
            ]
application = tornado.web.Application(handlers)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()