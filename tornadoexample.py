#!/usr/bin/python
'''Starts and runs the server'''

# database imposrts
from pymongo import MongoClient

# tornado imports
import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

from basehandler import BaseHandler
import examplehandlers
import sklearnhandlers

# Setup information for tornado class
define("port", default=8000,
       help="run on the given port", type=int)

# Utility to be used when creating the Tornado server
# Contains the handlers and the database connection
class Application(tornado.web.Application):
    def __init__(self):
	'''Store necessary handlers,
	   connect to database
	'''

        handlers = [(r"/[/]?", BaseHandler),
                    (r"/Test[/]?",examplehandlers.TestHandler),
                    (r"/DoPost[/]?",examplehandlers.PostHandler),
    				(r"/Upload[/]?",examplehandlers.FileUploadHandler),
                    (r"/AddDataPoint[/]?",sklearnhandlers.UploadLabeledDatapointHandler),
                    (r"/GetNewDatasetId[/]?",sklearnhandlers.RequestNewDatasetId),
                    (r"/UpdateModel[/]?",sklearnhandlers.UpdateModelForDatasetId),     
                    (r"/PredictOne[/]?",sklearnhandlers.PredictOneFromDatasetId),               
                    ]

        settings = {'debug':True}
        tornado.web.Application.__init__(self, handlers, **settings)

        self.client  = MongoClient() # local host, default port
        self.db = self.client.sklearndatabase # database with labeledinstances, models

    def __exit__(self):
        self.client.close()


def main():
    '''Create server, begin IOLoop 
    '''
    tornado.options.parse_command_line()
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()
