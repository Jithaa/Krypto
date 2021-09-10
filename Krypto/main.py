from flask import Flask,request
from flask_restful import Api,Resource,reqparse,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import threading
RF={
	'sno':fields.Integer,
	'id':fields.String,
	'val':fields.Float,
	'status':fields.String,
	'name':fields.String		
}


def threaded(fn):
	def wrapper(*args, **kwargs):
		c=threading.Thread(target=fn, args=args, kwargs=kwargs,daemon=True).start()
		return c
	return wrapper

app=Flask(__name__)
api=Api(app)
alerts={}
alerts_args=reqparse.RequestParser()
alerts_args.add_argument("Value",type=float,help="Only Float is accepted",required=True)
alerts_args.add_argument("name",type=str,help="Only Float is accepted",required=True)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

class alerts_db(db.Model):
	
	sno=db.Column(db.Integer,primary_key=True,autoincrement=True)
	id=db.Column(db.String(100),nullable=False)
	val=db.Column(db.Float(100),nullable=False)
	status=db.Column(db.String(100),nullable=False)
	name=db.Column(db.String(100),nullable=False)
	def __repr__(self):
		return f"Data(sno={sno},id={id},val={val},status={status})"


class Data(Resource):
	
	@marshal_with(RF)
	def get(self,id):
		if id!="fetch_all":
			res=alerts_db.query.filter_by(status=id).limit(50).all()
		else:
			res=alerts_db.query.filter_by().limit(50).all()
		
				

		return res
		
	@marshal_with(RF)
	def put(self,id):
		if (id=="create"):
			
			args=alerts_args.parse_args()
			print(args['Value'])
			v=alerts_db(id=id,val=args['Value'],status="Created",name=args['name'])
			db.session.add(v)
			db.session.commit()
			return v,201
		elif (id=="delete"):
			args=alerts_args.parse_args()
			print(args['Value'])
			res=alerts_db.query.filter_by(val=args['Value']).limit(50).all()
			l=[]
			if type(res)==type(l):
				for i in res:
					try:
						db.session.delete(i)
						db.session.commit()
					except:
						return "NA"
			else:
				try:
					db.session.delete(res)
					db.session.commit()
				except:
					return "NA"
			
			v=alerts_db(id=id,val=args['Value'],status="Deleted",name=args["name"])
			db.session.add(v)
			db.session.commit()
			return v,201
	@threaded
	def uu(self):
		import time
		import hashlib
		import json
		import urllib.request
		from urllib.request import urlopen, Request
		def dodo(self):
			print("dodo")
			di={}
			operUrl = urllib.request.urlopen("https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false")
			if(operUrl.getcode()==200):
				data = operUrl.read()
				data=json.loads(data)
				
			else:
				print("Error receiving data", operUrl.getcode())

			for i in data:
				di[i['symbol']]=i['current_price']
			print(di)
			res=alerts_db.query.filter_by(status="Created").limit(50).all()
			print(res)
			l=[]
			if type(res)==type(l):
				for i in res:
					print(i['val'],d[i['name']])
					if i['val']==d[i['name']] :
						
						db.session.delete(i)
						db.session.commit()
						i['status']="Triggered"
						print(i)
						db.session.add(v)
						db.session.commit()
				else:
					if res['val']==d[res['name']] :
						db.session.delete(res)
						db.session.commit()
			
		
		def main(self):
			url = Request("https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false")

			response = urlopen(url).read()

			currentHash = hashlib.sha224(response).hexdigest()
			print("running")
			time.sleep(10)
			while True:
				
				try:
					response = urlopen(url).read()
					currentHash = hashlib.sha224(response).hexdigest()
					time.sleep(30)
					response = urlopen(url).read()
					newHash = hashlib.sha224(response).hexdigest()
					if newHash == currentHash:
						continue

					else:
						print("something changed")
						dodo()

						response = urlopen(url).read()
						print(response)
						currentHash = hashlib.sha224(response).hexdigest()
						time.sleep(30)
						continue
				
						
				# To handle exceptions
				except Exception as e:
					print("error")
				
		main()
			
		
		
api.add_resource(Data,"/alert/<string:id>")
if __name__ =="__main__":
	app.run()
	
