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

## 1. CTRL+C를 누르면 '복사라고 말해 줘요.

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
