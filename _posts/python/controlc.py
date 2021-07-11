from scriptHandler import script
import ui
import globalPluginHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
#	__gestures = {'kb:control+c': 'controlc'}
	@script(gesture='kb:control+c')
	def script_controlc(self, gesture):
		ui.message('복사')
		gesture.send()
