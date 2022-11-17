import sys
import telnetlib

class MyTelnet(telnetlib.Telnet):

	def listener(self):
		while 1:
			try:
				data = self.read_eager()
			except EOFError:
				print('*** Connection closed by remote host ***')
				return
			if data:
				sys.stdout.write(data.decode('euc-kr', 'ignore'))
			else:
				sys.stdout.flush()

	def interact(self):
		if sys.platform == "win32":
			self.mt_interact()
			return
		with _TelnetSelector() as selector:
			selector.register(self, selectors.EVENT_READ)
			selector.register(sys.stdin, selectors.EVENT_READ)

			while True:
				for key, events in selector.select():
					if key.fileobj is self:
						try:
							text = self.read_eager()
						except EOFError:
							print('*** Connection closed by remote host ***')
							return
						if text:
							sys.stdout.write(text.decode('euc-kr', 'ignore'))
							sys.stdout.flush()
					elif key.fileobj is sys.stdin:
						line = sys.stdin.readline().encode('euc-kr', 'ignore')
						if not line:
							return
						self.write(line)

t = MyTelnet()
t.open('bbs.kbuwel.or.kr')
t.interact()

