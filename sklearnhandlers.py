#!/usr/bin/python

from pymongo import MongoClient
import tornado.web

from tornado.web import HTTPError
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

from basehandler import BaseHandler

from sklearn.neighbors import KNeighborsClassifier
import pickle
from bson.binary import Binary

class UploadLabeledDatapointHandler(BaseHandler):
	def post(self):
		'''Save data point and class
		'''
		vals = self.get_argument("feature").split(',');
		fvals = [float(val) for val in vals];
		label = self.get_int_arg("label");
		sess  = self.get_int_arg("dsid",default=0);

		dbid = self.db.labeledinstances.insert(
			{"feature":fvals,"label":label,"dsid":sess}
			);
		self.write_json({"id":str(dbid),"feature":fvals,"label":label});
		#for a in db.labeledinstances.find(): print [float(val)*2 for val in a['feature']]

class RequestNewDatasetId(BaseHandler):
	def post(self):
		'''
		'''
		a = self.db.labeledinstances.find_one(sort=[("dsid", -1)])
		newSessionId = float(a['dsid'])+1;
		self.write_json({"dsid":newSessionId})

class UpdateModelForDatasetId(BaseHandler):
	def post(self):
		'''
		'''
		dsid = self.get_int_arg("dsid",default=0);
		# create feature vectors
		f=[];
		for a in self.db.labeledinstances.find({"dsid":dsid}): 
			f.append([float(val) for val in a['feature']])

		l=[];
		for a in self.db.labeledinstances.find({"dsid":dsid}): 
			l.append(a['label'])

		c1 = KNeighborsClassifier(n_neighbors=3);
		acc = -1;
		if l:
			c1.fit(f,l);
			lstar = c1.predict(f);
			acc = sum(lstar==l)/float(len(l));
			bytes = pickle.dumps(c1);
			self.db.models.update({"dsid":dsid},
				{  "$set": {"model":Binary(bytes)}  },
				upsert=True)

		self.write_json({"resubAccuracy":acc})

class PredictOneFromDatasetId(BaseHandler):
	def post(self):
		'''
		'''
		dsid = self.get_int_arg("dsid",default=0);
		vals = self.get_argument("feature").split(',');
		fvals = [float(val) for val in vals];

		tmp = self.db.models.find_one({"dsid":dsid})
		c2 = pickle.loads(tmp['model'])
		predLabel = c2.predict(fvals);
		self.write_json({"prediction":str(predLabel)})

