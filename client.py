#!/usr/bin/env python

import sys
from gntp.notifier import GrowlNotifier
from optparse import OptionParser

class ClientParser(OptionParser):
	def __init__(self,file):
		OptionParser.__init__(self)
		
		#Network
		self.add_option("-H","--host",help="Specify a hostname to which to send a remote notification. [%default]",
						dest="host",default='localhost')
		self.add_option("--port",help="port to listen on",
						dest="port",type="int",default=23053)
		self.add_option("-P","--password",help="Network password",
					dest='password',default='')
		
		#Required (Needs Defaults)
		self.add_option("-n","--name",help="Set the name of the application [%default]",
						dest="app",default='Python GNTP Test Client')
		self.add_option("-N","--notification",help="Set the notification name [%default]",
						dest="name",default='Notification')
		self.add_option("-t","--title",help="Set the title of the notification [Default :%default]",
						dest="title",default=None)
		self.add_option("-m","--message",help="Sets the message instead of using stdin",
						dest="message",default=None)
		
		#Optional (Does not require Default)
		self.add_option("-d","--debug",help="Print raw growl packets",
						dest='debug',action="store_true",default=False)
		self.add_option("-s","--sticky",help="Make the notification sticky [%default]",
						dest='sticky',action="store_true",default=False)
		self.add_option("-p","--priority",help="-2 to 2 [%default]",
						dest="priority",type="int",default=0)
		self.add_option("--image",help="Icon for notification (Only supports URL currently)",
						dest="icon",default='')
		self.add_option("-e","--edit",help="Open config in $EDITOR",
					dest='edit',action="store_true",default=False)
	def parse_args(self, args=None, values=None):
		values, args = OptionParser.parse_args(self, args, values)
		if values.edit: exit(self._config.editor())
		
		if values.message is None:
			print 'Enter a message followed by Ctrl-D'
			try: message = sys.stdin.read()
			except KeyboardInterrupt: exit()
		else:
			message = values.message
		
		if values.title is None:
			values.title = ' '.join(args)
		
		# If we still have an empty title, use the 
		# first bit of the message as the title
		if values.title == '':
			values.title = message[:20]
		
		return values, message

if __name__ == "__main__":
	(options,message) = ClientParser('~/.gntp').parse_args()
	
	growl = GrowlNotifier(
		applicationName = options.app,
		notifications = [options.name],
		defaultNotifications = [options.name],
		hostname = options.host,
		password = options.password,
		port = options.port,
		debug = options.debug,
	)
	result = growl.register()
	if result is not True: exit(result)
	
	result = growl.notify(
		noteType = options.name,
		title = options.title,
		description = message,
		icon = options.icon,
		sticky = options.sticky,
		priority = options.priority,
	)
	if result is not True: exit(result)

