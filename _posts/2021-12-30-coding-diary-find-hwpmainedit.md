---
title: "코딩 일기 - Hwp2022 Plugin For NVDA - 메인편집창을 찾아라 예제 소스 코드"
excerpt: ""
categories: "blog"
toc: true
date: 2021-12-30
last-modified-at: 2021-12-30
---

# 코딩 일기 - 2021년 12월 30일

## 메일 편집창을 찾아 보자

파일: hwp/__init__.py

```python
# 한글2022를 지원하기 위한 플러그인
# 작성자 : 장창환

import appModuleHandler
import controlTypes
import tones
from NVDAObjects.behaviors import *
from textInfos.offsets import *

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == 'HwpMainEditWnd':
			clsList.insert(0, HwpMainEdit)



class HwpMainEditTextInfo(OffsetsTextInfo):
	def _getSelectionOffsets(self):
		return 0, 0

	def _getStoryText(self):
		return ''
	def _getStoryLength(self):
		return 1



class HwpMainEdit(EditableTextWithAutoSelectDetection):
	TextInfo = HwpMainEditTextInfo
	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT

	def event_caret(self):
		tones.beep(1000, 50)
		super(HwpMainEdit, self).event_caret()


	def _get_states(self):
		states = super(HwpMainEdit, self).states
		states.add(controlTypes.STATE_MULTILINE)
		return states


	def _get_name(self):
		return ''


```
