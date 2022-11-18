---
title: "파이썬에 빠져 봅시다."
excerpt: ""
categories: "blog"
toc: true
date: 2022-11-17
last-modified-at: 2022-11-17
---



# 파이썬에 빠져 봅시다.

## 왜 하필이면 파이썬 언어인가요?

- 어떤 언어보다도 문법이 쉽습니다.
- 라이브러리가 방대합니다.

이 두 가지 장점을 조합하면 이런 결과가 나옵니다.

남들이 만들어 놓은 소스 코드를 손쉽게 응용할 수 있다는 말씀.

### 먼저 웹서버를 하나 구동해 봅시다.

최신 64비트 파이썬은 [여기](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe)에서 다운로드하고 설치하세요. 설치할 때 약간 고려할 것이 있습니다만, 시간 관계상 생략할께요.

윈도우 키를 누르고 cmd를 입력한 후 엔터키를 누릅니다. 그러면 명령 프롬프트가 열립니다. 다음과 같이 입력하고 엔터키를 누릅니다.

python -m http.server 8080

8080 포트로 접속할 수 있는 간단한 웹서버가 구동되었습니다. 크롬을 열고 주소 입력창에 이렇게 써 보아요.

localhost:8080

웹페이지가 열리나요? 왠 폴더 이름들이 나타납니다. 이곳은 사용자의 홈폴더입니다. 여기에 index.html 파일을 추가하고 위 주소로 접속하면 정상적인 웹페이지가 나타날 겁니다. 신기하죠.

꼭 파이썬 문법을 몰라도 바로 써 먹을 수 있는 기능입니다. 접근성 공부하시는 분들 이 기능한 번 써 보시죠. 정말 편할 겁니다.

그럼 이번에는 조금 코딩다운 것을 해 봅시다. 

### 넓은마을 같은 텔넷 프로그램을 한번 만들어 볼까요? 처음부터 모든 것을 만들 필요가 없습니다. 남들이 잘 만들어 놓은 걸 고칠 줄 알면 됩니다.

'''python

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

'''

메모장에 위 내용을 복사해 넣고 telnet.py라고 저장합시다. 그리고 명령 프롬프트에서 이렇게 입력합시다.

python telnet.py

신기하죠? 넓은마을이 나타납니다. 실제로는 딱 3줄이면 되는데 아쉽게도 한글처리 때문에 몇 군데를 고쳐야 했습니다. 아쉽죠.

파이썬은 좀 더 복잡한 윈도우용 프로그램도 만들 수 있어요. 바로 초록멀티가 그 좋은 예입니다. 한번 실행해 볼까요?

파이썬으로 스마트폰 앱을 만들기 어렵다는 단점이 지적되어 왔습니다. 최근 키비(kivy), 비웨어(beeware) 등과 같은 프레임워크가 나와서 스마트폰 앱을 쉽게 만들 수 있도록 노력하기 시작했어요.

또 파이썬에는 이런 장점도 있습니다.

### 다양한 코딩 스타일을 지원합니다.

C#이나 자바 같은 훌륭한 프로그램은 이른바 객체지향 스타일의 코딩을 해야 합니다. 하지만 파이썬은 그렇게 어려운 것은 몰라도 쉽게 프로그램을 만들 수 있습니다. 

### 계산기를 만들어 볼까요?

'''python

s = input('수식 입력:')
print(eval(s))

'''

이렇게 간단하게 만들 수 있습니다. 계산을 반복하고 싶다구요. 이렇게 하세요.

'''python

while 1:
	s = input('수식 입력:')
	if not s: break
	print(eval(s))

'''

이 소스 코드를 메모장에 복사하고 calc.py로 저장하세요. 그리고 이렇게 실행해 봅시다.

python calc.py

참 쉽죠? 파이썬은 이렇게 간단한 형태로도 프로그램을 만들 수 있습니다.

### 파이썬은 다양한 언어와 혼합됩니다.

C#이 부러우신가요?  그렇다면 IronPython은 어떠신가요? C#이 사용하는 닷넷 라이브러리를 파이썬에서 그대로 사용할 수 있습니다. 더 쉽게 말이죠. 자바가 부러우신가요? 자이썬(jython)도 있습니다. 최근에는 자바스크립트와 혼합이 된 브리썬(brython)도 있다고 하네요.

### 파이썬은 윈도우즈, 리눅스, 맥용 프로그램을 모두 만들 수 있어요.

## 결론은 이렇습니다.

배우기 쉽고, 많이 활용할 수 있는 언어.

그것이 파이썬입니다.
