#!/usr/bin/env python
from __future__ import print_function

import socket
import sys
import json
sys.path.append('./gen-py')

from helloworld import HelloWorld
from helloworld.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# import pygn library
from pygn import pygn

clientID = '173703779-EA19716F8D2A73DF7ECAF522D5050BF3' # Enter your Client ID from developer.gracenote.com here
userID = pygn.register(clientID) # Get a User ID from pygn.register() - Only register once per end-user

mood_dic = {
"peaceful" : "65322",
"still" : "65322",
"romantic" : "65323",
"fantastic" : "65323",
"sentimental" : "65324",
"melting" : "65324",
"mushy": "65324",
"tender" : "42942",
"soft" : "42942",
"easygoing" : "42946",
"happy" : "42946",
"relaxed" : "42946",
"leisurable" : "42946" , 
"yearning" : "65325",
"eager":"65325",
"hungry": "65325",
"desired": "65325",
"anxious": "65325",
"sick": "65325",
"sophisticated" : "42954",
"experienced": "42954",
"sensual" : "42947",
"lay": "42947",
"cool" : "65326",
"calm": "65326",
"gritty" : "65327",
"somber" : "42948",
"severe": "42948",
"blue": "42948",
"dark": "42948",
"lowering": "42948",
"melancholy" : "42949",
"sad": "42949",
"serious" : "65328",
"solemn": "65328",
"brooding" : "65329",
"reflecting": "65329",
"fiery" : "42953",
"passionate": "42953",
"hotter": "42953",
"urgent" : "42955",
"instant": "42955",
"defiant" : "42951",
"challenging": "42951",
"aggressive" : "42958",
"invasive": "42958",
"enterprising": "42958",
"rowdy" : "65330",
"clamorous" : "65330",
"excited" : "42960",
"active": "42960",
"living": "42960",
"hot": "42960",
"energizing" : "42961",
"motivating": "42961",
"urging": "42961",
"empowering" : "42945",
"stirring" : "65331",
"engaged": "65331",
"lively" : "65332",
"alive": "65332",
"sincere": "65332",
"upbeat" : "65333",
"optimistic" : "65333",
"rising": "65333",
"other" : "42966"
}



class HelloWorldHandler:
	def ping(self):
		return "pong"

	def say(self, msg):
		keyword = msg
		moodid = ''
		output = ''
		if not mood_dic.has_key(keyword):
			ret = 'Received: ' + 'No available keywords in databases'
			return ret
		else:
			moodid = mood_dic[keyword]
		# Example how to create a radio playlist by artist and track
		results = pygn.createRadio(clientID, userID, artist='', track='', mood=moodid, popularity ='1000', similarity = '1000', count = '2')
		output = "Song for " + keyword + ":\n"
		if results == None:
			output = 'No available tracks in databases'
		for result in results:
			output += 'Track title: ' + result['track_title'] + ', Artist: '+result['album_artist_name']
		ret = "Received: " + output
		print(ret)
		return ret

handler = HelloWorldHandler()
processor = HelloWorld.Processor(handler)
transport = TSocket.TServerSocket("localhost", 9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print("Starting thrift server in python...")
server.serve()
print("done!")
