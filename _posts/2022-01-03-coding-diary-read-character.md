---
title: "코딩 일기 - 이제 글자 정도는 읽어 줘야지~"
excerpt: ""
categories: "blog"
toc: true
date: 2021-01-03
last-modified-at: 2021-01-03
---

# 코딩 일기 - 2021년 1월 3일 (월)

## IHncAADocument 개발자 가이드 문서

https://drive.google.com/file/d/1mStBWurV_C0mWx7H_9z8TfpepPpierVi/view?usp=sharing

### 파일: mainEdit.py

```python
from ctypes import *
import ui
import oleacc
import controlTypes
import tones
from NVDAObjects.behaviors import *
from .mainEditTextInfo import HwpMainEditTextInfo
from comtypes.automation import *
from comtypes.automation import _ctype_to_vartype
from comtypes.client.dynamic import *

_ctype_to_vartype[POINTER(IDispatch)] = VT_BYREF | VT_DISPATCH

class HwpMainEdit(EditableTextWithAutoSelectDetection):
	TextInfo = HwpMainEditTextInfo
	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT


	def _get_states(self):
		states = super(HwpMainEdit, self).states
		states.add(controlTypes.STATE_MULTILINE)
		return states


	def _get_name(self):
		return ''

	def _get_aa(self):
		if not getattr(self, '_aa', None):
			p = oleacc.AccessibleObjectFromWindow_safe(self.windowHandle, 0x41060001, IDispatch)
			self._aa = Dispatch(p)
		return self._aa


	def script_caret_moveByCharacter(self, gesture):
		gesture.send()
		p = POINTER(IDispatch)()
		self.aa.get_haccParaPosByCaret(byref(p))
		bstr = BSTR()
		n = c_long()
		self.aa.get_haccParaTextByParaPos(p, byref(bstr), byref(n))
		s = bstr.value
		num = n.value
		ui.message(s[num])
```


### 파일: mainEditTextInfo.py

```python
from textInfos.offsets import *


class HwpMainEditTextInfo(OffsetsTextInfo):
	def _getSelectionOffsets(self):
		return 0, 0

	def _getStoryText(self):
		return ''
	def _getStoryLength(self):
		return 1
```

### 파일: hwp/__init__.py



```python
# 한글2020를 지원하기 위한 플러그인
# 작성자 : 장창환

import appModuleHandler
from .mainEdit import HwpMainEdit


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == 'HwpMainEditWnd':
			clsList.insert(0, HwpMainEdit)
```

