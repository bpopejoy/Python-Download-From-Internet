import socket # Needed to recieve image
from cStringIO import StringIO # Needed to load image data into buffer.
import pygame as pg,sys,os,time # Needed to display image/time.

def main():
	# Sets up socket.
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	connect_to_valid_server(s)
	
	# Requests and receives images.
	print 'Getting background image...'
	backgroundPic=request_and_recv_image(s,'bg')
	print 'Getting pointer image...'
	pointerPic=request_and_recv_image(s,'pointer')
	if 1:# To test with a large image (2048x2048)
		print 'Getting large sample image...'
		largeI=request_and_recv_image(s,'large')
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	print 'Launching application...'
	
	# Sets up pygame and displays image/time.
	pg.init()
	pg.mouse.set_visible(False)
	fpsClock = pg.time.Clock()
	font = pg.font.Font('freesansbold.ttf',26)
	mouseP=(0,0)
	point=(5000,5000)
	seconds=False
	window = pg.display.set_mode((backgroundPic.get_rect().size[0],backgroundPic.get_rect().size[1]))
	while 1:
		window.blit(backgroundPic,(0,0))
		window.blit(pointerPic,mouseP)
		if seconds:
			msgObj=font.render("It is {}".format(time.strftime("%H:%M:%S")), 1, pg.Color(0,0,0))
		else:
			msgObj=font.render("It is {}".format(time.strftime("%H:%M")), 1, pg.Color(0,0,0))
		window.blit(msgObj,point)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sys.exit()
			elif event.type == pg.MOUSEMOTION:
				mouseP = event.pos
			elif event.type == pg.MOUSEBUTTONUP:
				if event.button in (1,2):
					point = event.pos
				elif event.button==3:
					point=(5000,5000)
				else:
					seconds=not seconds
		pg.display.update()
		fpsClock.tick(60)

def connect_to_valid_server(s,port=55550):# Connects to first open server in range from 55550 to 55559.
	try:#							If none of those servers are available, then quits application.
		s.connect(('',port))
		print 'Connected to server on port {}.'.format(port)
	except socket.error:
		if port<55560:
			connect_to_valid_server(s,port+1)
		else:
			s.close()
			print 'Could not find server. Closing application.'
			sys.exit()

def request_and_recv_image(s,image_str):
	# Requests image from server.
	s.send(image_str)
	# Records the amount of data being sent.
	lenData=int(s.recv(1024))
	# Sends signal to server telling it that it's ready to recv data.
	s.send(' ')
	data=''
	count=0# DELETE_ME
	# Keep recving data until it is the specified length, adding it to the rest of the data each time.
	while len(data)<lenData:
		count+=1 #DELETE_ME
		tmpData=s.recv(lenData-len(data))
		data+=tmpData
	# Forms image from data.
	print count# DELETE_ME
	return pg.image.load(StringIO(data))

if __name__=='__main__':
	main()
