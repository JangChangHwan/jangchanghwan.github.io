---
title: "코딩 일기 - 플러그인을 플러그인 답게"
excerpt: ""
categories: "blog"
toc: true
date: 2021-01-06
last-modified-at: 2021-01-06
---

# 코딩 일기 - 2021년 1월 6일 목월)

### 파일: idispatch.py

```python

from ctypes import *
from comtypes import *
from comtypes.automation import *
from comtypes.automation import _ctype_to_vartype
from comtypes.client.dynamic import *


class HwpIDispatch(IDispatch):
	@property
	def lpp(self):
		v = VARIANT()
		obj = Dispatch(self)
		obj.GetItem('List', byref(v))
		li = v.value
		obj.GetItem('Para', byref(v))
		pa = v.value
		obj.GetItem('Pos', byref(v))
		po = v.value
		return (li, pa, po)

	def __eq__(self, other):
		return self.lpp == other.lpp



_ctype_to_vartype[POINTER(HwpIDispatch)] = VT_BYREF | VT_DISPATCH

```

### 파일: mainEdit.py

```python

from .idispatch import *
import oleacc
import controlTypes
from .mainEditTextInfo import HwpMainEditTextInfo
from NVDAObjects.behaviors import *


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
			p = oleacc.AccessibleObjectFromWindow_safe(self.windowHandle, 0x41060001, HwpIDispatch)
			self._aa = Dispatch(p)
		return self._aa

```


### 파일: mainEditTextInfo.py

```python

from .idispatch import *
from textInfos.offsets import *


class HwpMainEditTextInfo(OffsetsTextInfo):
	def _getSelectionOffsets(self):
		return 0, 0

	def _getStoryText(self):
		return ''
	def _getStoryLength(self):
		return 1

	def _getCaretOffset(self):
		p = POINTER(HwpIDispatch)()
		self.obj.aa.get_haccParaPosByCaret(byref(p))
		return p

	def _getCharacterOffsets(self, offset):
		p = POINTER(HwpIDispatch)()
		self.obj.aa.get_haccParaPos(1, offset, byref(p))
		if not bool(p):
			p = offset
		return offset, p

	def _getTextRange(self, start, end):
		bstr = BSTR()
		n = c_long()
		self.obj.aa.get_haccRangeText(start, end, byref(bstr), byref(n))
		rangeText = bstr.value
		return rangeText if bool(rangeText) else ''

```

