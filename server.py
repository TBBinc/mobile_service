import cherrypy
import os
from dotenv import load_dotenv
from os.path import join, dirname

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class MobileServer(object):

	def __init__(self, session):
		self.session = session

	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self):
		return {
			"apiversion" : "1",
			"author":"Arik Barenboim"
		}

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def location(self):
		data = cherrypy.request.json
		print(data)
		session.execute(
			"""
			INSERT INTO users.location_info(latlocation, longlocation, age, pushToken)
			VALUES (%s,%s,%s,%s)
			""",
			(data['latlocation'],data['longlocation'],data['age'],data['pushToken'])
		)
		return { "status" : "success"}


if __name__ == "__main__":

	dotenv_path = join(dirname(__file__), '.env')
	load_dotenv(dotenv_path)

	cloud_config= {'secure_connect_bundle': os.getenv('PATH_TO_ZIP')}
	auth_provider = PlainTextAuthProvider(os.getenv('ASTRA_DB_USERNAME'), os.getenv('ASTRA_DB_PASSWORD'))
	cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
	session = cluster.connect()

	server = MobileServer(session)
	cherrypy.config.update({"server.socket_host": "127.0.0.1"})
	cherrypy.config.update(
		{"server.socket_port": int(os.environ.get("PORT", "8080")),}
	)
	print("Starting Mobile Server...")
	cherrypy.quickstart(server)