from socket import *
import pickle

serverPort = 6501
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

class registrated:
	def __init__(self, inName, inIP, inPort):
		self.inName = inName
		self.inIP = inIP
		self.inPort = inPort	

class contactList:
	def __init__(self, name):
		self.name = name
		self.users = []

class imInstance:
	def __init__(self, contactList, contactName):
		self.contactList = contactList
		self.contactName = contactName

registerList = [] #for the structs
registerCN = [] #just for the names. makes searching easier
CL = [] #emptyList for contact lists
imList = [] #list for contacts that have started im

print("The server is ready to receive")
#loop to continue to run server
while True:
	message, clientAddress = serverSocket.recvfrom(2048)
	receivedMessage = message.decode()
	x = receivedMessage.split()
	succFail = "SUCCESS"

	#block to handle registering
	if x[0] == 'register':
		print('register')
		if x[1] in registerCN:
			succFail = "FAILURE"
		else:
			registerCN.append(x[1])
			newUser = registrated(x[1], x[2], x[3])
			registerList.append(newUser)

	#block to handle creating
	elif x[0] == 'create':
		print('create')
		newList = contactList(x[1])
		CL.append(newList)
		print("The number of contact-lists is " + str(len(CL)))

		#Search through to prevent duplicates		

	#block to handle joining
	elif x[0] == 'join':
		print('join')
		isIm = 0
		for y in imList:
			if(y.contactName == x[1]):
				print("Cannot join! Contact is in IM")
				isIm = 1
				succFail = "FAILURE"	
	
		if isIm == 0:
			for x3 in registerList:
				if(x3.inName == x[2]):
					print('Found in registerList')
					toBeAdded = x3
				else:
					print('Not in registerList')
			
			for x2 in CL:
				if(x2.name == x[1]):
					print('Contact List Exists')
					x2.users.append(toBeAdded)
					print('user appended to list')
					print(str(len(x2.users)))
				else:
					print("It was not a match")

	#block to handle list query
	elif x[0] == 'query-lists':
		print('query-lists')
		print('# of Lists: ' + str(len(CL)))
		queried = '# of Lists: ' + str(len(CL))
		for y in range(len(CL)):
			print(CL[y].name)
			q2 = CL[y].name
			queried = queried + "\n" + str(q2)
		serverSocket.sendto(queried.encode(), clientAddress)
	
	#block to handle saving
	elif x[0] == 'save':
		print('save')
		f = open(x[1], 'w+')
		#f.write('testing')
		f.write("The number of contacts is " + str(len(registerList)))
		for user in registerList:
			f.write("\n" + user.inName + " "  + user.inIP + " " +  user.inPort)
		f.write("\nThe number of contact lists is " + str(len(CL)))
		for lists in CL:
			f.write("\n" + lists.name)
			for ILU in lists.users:
				f.write('\n\t' + ILU.inName + ' ' +  ILU.inIP + ' ' + ILU.inPort) 
		f.close()
	
	#block to handle exiting
	elif x[0] == 'exit':
		print('exit')
		isIm = 0
		for y in imList:
			if(y.contactName == x[1]):
				print("Cannot exit! Contact is in IM")
				isIm = 1;
				succFail = "FAILURE"
		if isIm == 0:
		#Remove from Registereted names
			registerCN.remove(x[1])
		#Remove from contact lists
			for x2 in CL:
				print("removing " + x[1] +  "!")
				for x3 in x2.users:
					if (x3.inName == x[1]):
						x2.users = [item for item in x2.users if item.inName != x[1]]
		#remove from RegisterList
			for x4 in registerList:
				print("removing " + x[1] + "!")
				if (x4.inName == x[1]):
					registerList = [item for item in registerList if item.inName != x[1]]

	#block to handle leaving
	elif x[0] == 'leave':
		isIm = 0
		for y in imList:
                        if(y.contactName == x[1]):
                                print("Cannot leave! Contact is in IM")
                                isIm = 1;
                                succFail = "FAILURE"
		print('leave')
		if isIm == 0:
			for x2 in CL:
				print("attempting to remove " + x[2] + " from " + x[1])
				if (x2.name == x[1]):
					print("Contact-List exists")
					for x3 in x2.users:
						if (x3.inName == x[2]):	
							print("We have a match!")
							succFail = "Success"
							x2.users = [item for item in x2.users if item.inName != x[2]]
	
			print(succFail) 

	#block to start the instant messaging
	elif x[0] == 'im-start':
		print("Received an im-start command!")
		newIm = imInstance(x[1], x[2])
		imList.append(newIm)
		for y in CL:
			if (y.name == x[1]):
				variable = y
		data_string = pickle.dumps(variable)
		serverSocket.sendto(data_string, clientAddress)

		# Calls broadcast function to send message to all  
        message_to_send = "<" + address + "> " + message  
        broadcast(message_to_send, conn) 
	
	#block to complete the instant messaging
	elif x[0] == 'im-complete':
		print("received an im-complete command!")
		for y in imList:
			print("removing the im from the list of active ims")
			imList = [item for item in imList if (item.contactList != x[1] and item.contactName != x[2])]
	else:
		print('ERROR')
		succFail = "FAILURE"
		
	serverSocket.sendto(succFail.encode(), clientAddress)

#broadcast to all clients except sender	
def broadcast(message, clientAddress):  
    for client in CL:  
        if client!=clientAddress:  
            try:  
                client.send(message)  
            except:  
                client.close()  
  
                # if link is broken, we remove the client  
                remove(client)  