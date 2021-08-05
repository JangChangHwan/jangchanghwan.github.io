---
title: "NVDA 플러그인 개발자 안내서 예제 모음"
excerpt: ""
categories: "blog"
toc: true
date: 2021-01-01
last-modified-at: 2021-07-10
---

# NVDA 플러그인 개발자 안내서 예제 모음

이 예제들은 NVDA 플러그인 개발자 안내서 동영상에 나오는 예제들입니다.

## 1. CTRL+C를 누르면 '복사라고 말해 줘요: 

위치: globalPlugins/

이름: controlc.py

### 예전 스타일 방식: __gestures 활용

```python
import ui
import globalPluginHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	__gestures = {'kb:control+c': 'controlc'}

	def script_controlc(self, gesture):
		ui.message('복사')
		gesture.send()

```


### 새로운 방식: @script 활용

```python
from scriptHandler import script
import ui
import globalPluginHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	@script(gesture='kb:control+c')
	def script_controlc(self, gesture):
		ui.message('복사')
		gesture.send()
```


## 2. 메모장 비언~ 시이인~~

위치: appModules/

이름: notepad.py

```python
import tones
import ui
import json
import urllib
import textInfos
import api
import appModuleHandler
from scriptHandler import script

class AppModule(appModuleHandler.AppModule):
	@script(gesture='kb:nvda+f8')
	def script_checkSpellOut(self, gesture):
		editObj = api.getCaretObject()
		info = editObj.makeTextInfo(position=textInfos.POSITION_CARET)
		info.expand(unit=textInfos.UNIT_PARAGRAPH)
		paraText = info.text
		data = 'text1=' + paraText
		data = data.encode('utf8')
		res = urllib.request.urlopen('https://speller.cs.pusan.ac.kr/results', data)
		htm = res.read().decode('utf8')
		start = htm.find('data = [{')
		if start == -1:
			tones.beep(1000, 100)
			return
		end = htm.find('}];', start)
		errData = htm[start+7:end+2]
		errObj = json.loads(errData)
		errList = errObj[0]['errInfo']
		resultList = ['틀린 문구: %s\n추천 문구: %s\n도움말: %s' % (d['orgStr'], d['candWord'], d['help']) for d in errList]
		ui.browseableMessage('\n'.join(resultList), '맞춤법 검사 결과')
```


## 3. 메모장만 편애하면 안 돼요.


위치: globalPlugins/

이름: speller.py

```python
import inputCore
import ui
import json
import urllib
import textInfos
import api
import globalPluginHandler
from scriptHandler import script

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(gesture='kb:nvda+f8', description='맞춤법을 검사합니다.', category=inputCore.SCRCAT_MISC)
	def script_checkSpellOut(self, gesture):
		info = api.getReviewPosition()
		info.expand(unit=textInfos.UNIT_PARAGRAPH)
		paraText = info.text
		if not paraText.strip():
			ui.message('검사할 문자열이 없습니다.')
			return
		data = 'text1=' + paraText
		data = data.encode('utf8')
		res = urllib.request.urlopen('https://speller.cs.pusan.ac.kr/results', data)
		htm = res.read().decode('utf8')
		start = htm.find('data = [{')
		if start == -1:
			ui.message('맞춤법이 정확합니다.')
			return
		end = htm.find('}];', start)
		errData = htm[start+7:end+2]
		errObj = json.loads(errData)
		errList = errObj[0]['errInfo']
		resultList = ['틀린 문구: %s\n추천 문구: %s\n도움말: %s' % (d['orgStr'], d['candWord'], d['help']) for d in errList]
		ui.browseableMessage('\n'.join(resultList), '맞춤법 검사 결과')
```

## 5. 왜 말을 잘라먹니?

위치: appModules\

이름: notepad.py

```python
from NVDAObjects.window.edit import EditTextInfo
import appModuleHandler

class AppModule(appModuleHandler.AppModule):
	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == 'Edit':
			obj.TextInfo = NewEditTextInfo

class NewEditTextInfo(EditTextInfo):
	useUniscribe = False
```

