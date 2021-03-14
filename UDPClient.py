from socket import *
import pickle
serverName = '10.120.70.145'
serverPort = 6501
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('', 6502))

#holds registered users
class registrated:
	def __init__(self, inName, inIP, inPort):
		self.inName = inName
		self.inIP = inIP
		self.inPort = inPort

#holds name of lists and Registrated
class contactList:
	def __init__(self, name):
		self.name = name
		self.users = []
while True:
	message = input(':')
	
	clientSocket.sendto(message.encode(), (serverName, serverPort))
	receivedMessage, serverAddress = clientSocket.recvfrom(2048)
	y = message.split()
	#handles start of instant messaging
	if y[0] == "im-start":
		dataVariable = pickle.loads(receivedMessage)
		print(dataVariable.name)
		for z in dataVariable.users:
			if (z.inName == y[2]):
				sender = z
		dataVariable.users = [item for item in dataVariable.users if item.inName != y[2]]
		dataVariable.users.insert(0, sender)
		
		for x2 in dataVariable.users:
			print(x2.inName + ' ' + x2.inIP + ' ' + x2.inPort)

		imMessage = input('m:')
		
		#clientSocket.sendto(imMessage.encode(), (dataVariable.users[1].inIP, int(dataVariable.users[1].inPort)))
		clientSocket.sendto(imMessage.encode(), ('10.120.70.117', 6502))
	
		imComplete = "im-complete " + y[1] + " " + y[2]
		clientSocket.sendto(imComplete.encode(), (serverName, serverPort))
	else:
		x = receivedMessage.decode()
		print(receivedMessage.decode())
		#print(y[0])
		if y[0] == 'exit' and x == 'SUCCESS':
			clientSocket.close()
			break
