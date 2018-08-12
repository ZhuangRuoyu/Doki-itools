#coding=utf-8
import _tkinter ## import Tkinter as tk
import tkinter as tk ##
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import sys
import threading
import requests
# 下面几个包都是FirefoxProfile需要的
import copy
import json
import tempfile
import shutil
import os
import queue ## import Queue
# 这里将该json文件里的内容都放到了我们的脚本里，你也可以放到另一个py文件中import进来

## other libraries for login
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from urllib.request import urlretrieve
from PIL import Image

WEBDRIVER_PREFERENCES = """
{
  "frozen": {
	"app.update.auto": false,
	"app.update.enabled": false,
	"browser.displayedE10SNotice": 4,
	"browser.download.manager.showWhenStarting": false,
	"browser.EULA.override": true,
	"browser.EULA.3.accepted": true,
	"browser.link.open_external": 2,
	"browser.link.open_newwindow": 2,
	"browser.offline": false,
	"browser.reader.detectedFirstArticle": true,
	"browser.safebrowsing.enabled": false,
	"browser.safebrowsing.malware.enabled": false,
	"browser.search.update": false,
	"browser.selfsupport.url" : "",
	"browser.sessionstore.resume_from_crash": false,
	"browser.shell.checkDefaultBrowser": false,
	"browser.tabs.warnOnClose": false,
	"browser.tabs.warnOnOpen": false,
	"datareporting.healthreport.service.enabled": false,
	"datareporting.healthreport.uploadEnabled": false,
	"datareporting.healthreport.service.firstRun": false,
	"datareporting.healthreport.logging.consoleEnabled": false,
	"datareporting.policy.dataSubmissionEnabled": false,
	"datareporting.policy.dataSubmissionPolicyAccepted": false,
	"devtools.errorconsole.enabled": true,
	"dom.disable_open_during_load": false,
	"extensions.autoDisableScopes": 10,
	"extensions.blocklist.enabled": false,
	"extensions.checkCompatibility.nightly": false,
	"extensions.logging.enabled": true,
	"extensions.update.enabled": false,
	"extensions.update.notifyUser": false,
	"javascript.enabled": true,
	"network.manage-offline-status": false,
	"network.http.phishy-userpass-length": 255,
	"offline-apps.allow_by_default": true,
	"prompts.tab_modal.enabled": false,
	"security.csp.enable": false,
	"security.fileuri.origin_policy": 3,
	"security.fileuri.strict_origin_policy": false,
	"security.warn_entering_secure": false,
	"security.warn_entering_secure.show_once": false,
	"security.warn_entering_weak": false,
	"security.warn_entering_weak.show_once": false,
	"security.warn_leaving_secure": false,
	"security.warn_leaving_secure.show_once": false,
	"security.warn_submit_insecure": false,
	"security.warn_viewing_mixed": false,
	"security.warn_viewing_mixed.show_once": false,
	"signon.rememberSignons": false,
	"toolkit.networkmanager.disable": true,
	"toolkit.telemetry.prompted": 2,
	"toolkit.telemetry.enabled": false,
	"toolkit.telemetry.rejected": true,
	"xpinstall.signatures.required": false,
	"xpinstall.whitelist.required": false
  },
  "mutable": {
	"browser.dom.window.dump.enabled": true,
	"browser.laterrun.enabled": false,
	"browser.newtab.url": "about:blank",
	"browser.newtabpage.enabled": false,
	"browser.startup.page": 0,
	"browser.startup.homepage": "about:blank",
	"browser.usedOnWindows10.introURL": "about:blank",
	"dom.max_chrome_script_run_time": 30,
	"dom.max_script_run_time": 30,
	"dom.report_all_js_exceptions": true,
	"javascript.options.showInConsole": true,
	"network.http.max-connections-per-server": 10,
	"startup.homepage_welcome_url": "about:blank",
	"startup.homepage_welcome_url.additional": "about:blank",
	"webdriver_accept_untrusted_certs": true,
	"webdriver_assume_untrusted_issuer": true
  }
}
"""


class FirefoxProfile(webdriver.FirefoxProfile):
	""" Rewrite FirefoxProfile, to avoid 'No such file ... webdriver.xpi/pref.json' exception"""
	def __init__(self, profile_directory=None):
		if not FirefoxProfile.DEFAULT_PREFERENCES:
			FirefoxProfile.DEFAULT_PREFERENCES = json.loads(WEBDRIVER_PREFERENCES)

		self.default_preferences = copy.deepcopy(
			FirefoxProfile.DEFAULT_PREFERENCES['mutable'])
		self.native_events_enabled = True
		self.profile_dir = profile_directory
		self.tempfolder = None
		if self.profile_dir is None:
			self.profile_dir = self._create_tempfolder()
		else:
			self.tempfolder = tempfile.mkdtemp()
			newprof = os.path.join(self.tempfolder, "webdriver-py-profilecopy")
			shutil.copytree(self.profile_dir, newprof,
							ignore=shutil.ignore_patterns("parent.lock", "lock", ".parentlock"))
			self.profile_dir = newprof
			self._read_existing_userjs(os.path.join(self.profile_dir, "user.js"))
		self.extensionsDir = os.path.join(self.profile_dir, "extensions")
		self.userPrefs = os.path.join(self.profile_dir, "user.js")

	def update_preferences(self):
		for key, value in self.DEFAULT_PREFERENCES['frozen'].items():
			self.default_preferences[key] = value
		self._write_user_prefs(self.default_preferences)

	def add_extension(self, extension=os.path.abspath('webdriver.xpi')):
		self._install_extension(extension)


all_talks = u"""
『人生旅程很短，因此不妨去大胆一些，去爱一个人，去攀一座山，去追一个梦』
『睁开眼看到全世界，闭上眼只能看见你。』『一腔孤勇，一生只用于一处。』
 今天也好喜欢你。要加油哦
『纵然被命运铁蹄狠狠践踏，也顽强的长出自己的根芽。
『这里荒芜寸草不生，后来你来这走了一遭，奇迹般万物生长，这里是我的心
『你要相信自己，生来如同璀璨的夏日之花，不凋不败，妖冶如火。』
『总有一个人，会把你百炼钢化为绕指柔，教会你温柔对待这个世界。』
不要害怕意中人们陪你大闹天宫
『黄羚羊需要空地，天空需要颜色，你需要我。』
意中人们陪你到最后
『不要承诺，不是我不信，是我怕老天嫉妒。』『眸如水影亦随，陌上晚晴眉。』
这辈子我算是栽在你手里啦『
誓此生共君醉，千古莫相摧。』
加油盖世英雄。
『后来时间都与你有关，还好是你，成为我的喜欢。』
『我往时间里看一眼，只能看到你。
当我看你第一眼，便看到后来整片时间。』睁开眼看到全世界，闭上眼只能看见你。』
『风雨里像个大人，阳光里像个孩子。』
我们守护你的微笑，别害怕一切有我们。
你是我时间流走后，最想看的单纯。
谢谢你出现在我的身边。
你是我时间流走后，最想看的单纯。谢谢你出现在我的身边。
『 有一种回忆，永远含苞待放的美。
	有一种岁月， 年轮一样茶色蔓延。
	有一种容颜，停驻心底鲜明如斯。
	有一种人，万人万年之中，只需一眼，便知是你。』
『我们都曾不堪一击，但我们终将刀枪不入。』
『除非黄土白骨，我守你百岁无忧。』
『如果有遗憾，那也是遗憾没有再多爱你一点。』
瘦影自怜秋水照，卿须怜我我怜卿。伊人是那天上星，照我心中一轮月。
我也曾把光阴浪费，甚至莽撞到视死如归，只因爱上你，我才渴望长命百岁。
爱是把心放在了中间，把你放在了上面，把我放在最低的地方，我爱你，就是这样了吧。
喜欢你到整个世界森林里的老虎全部融化成黄油[心]
我的涵，你是那样的美，美得像一首抒情诗。你全身充溢着少女的纯情和青春的风采。
希望每晚星亮入梦时，有人来代替我吻你
那天空的乌云，因为涵涵你，我看见了雨后彩虹，从此，不怕风雨。
意涵就是这条街最靓的仔，无论走到哪都是最靓丽的风景线，意涵，我爱你
天空，大海都是蓝色，都有包容一切的温柔，意中人愿为你包容一切，换你眉欢眼笑
那清冷的寒风，因为涵涵你，我身着单薄衣裳也不觉冷，从此，心中有阳光。
人生自是有情痴，此恨不关风与月。一遇我涵误终身，便是西施也黯然
那街边的霓虹灯光，因为涵涵你，我看见了人间繁华，从此，不怕闹市烦扰。
我真的不敢看向陈意涵的眼睛 我怕她眼底的温柔融化了
我不知道你最近好吗？但我知道，我想你的时候，你就会收到思念。
我的思念和我的祈祷，都会换成一点点的幸运，让你一世无忧！
意中人是深深的大海,而你是那自海的另一边升起的曙光,永远照亮着我们。
你的气息是琐窗朱户的锦瑟，是花落水流红的丝缕杂质，是芳尘余存的袅袅雾霭，是满城风絮的闲愁万种。
无关风月，只得心下了然绽放的烟火，与味甜却生性寒凉的禁果。
与涵初相识，犹如故人归。与涵再相见，便是金风玉露一相逢，胜却人间无数。
该说的都说的清楚了，何必掩饰呢.意中人陈意涵，不需要掩饰.
常言道，爱人者，人恒爱之。你爱着人们，也会受到人们的爱。这份爱，不分你我，永恒
你笑的时候，彻夜未眠的海棠花，湖畔堆烟的杨柳，拂面的风夹裹着的逐水飞絮
凌波不过月台花榭的堇碟，梅子黄时雨，都为你停驻，而后更为跃动的舞上一曲。
希望每晚星亮入梦时，有人来代替我吻你
我看着东边的日出西边的雨，挂念远方的天气和心里的你@
那天空中的你，照耀我心房也是足够温暖
南风过境，春风十里不如你[心] -
谢谢你，让平凡的我能够成为另一个人的盖世英雄。
星星有多美，夜晚会知道。鱼儿有多美，海洋会知道。陈意涵有多美，我想让全世界知道。
春风十里，二十里，三十里，海底两万里，扶摇直上九万里
铁板烤里脊，芝士土豆泥，不如你，都不如你。[太开心]
原来盖世英雄也是普通人，但希望给你的温暖，无人能比。希望大闹天宫的日子，不负你
我不知道你最近好吗？但我知道，我想你的时候，你就会收到思念。
我的思念和我的祈祷，都会换成一点点的幸运，让你一世无忧
谢谢意涵的微笑，慌乱过我的年华
你就像是三棱镜，因为你平凡的阳光也能变成彩虹
喜欢你到整个世界森林里的老虎全部融化成黄油[心]
只缘我涵一回眸，使我思涵朝与暮。除非黄土白骨，我守涵百岁无忧。
莫问前程万里远，只管勇往无回头。天若有情天亦老，我若变心我枉生
哪里有什么百万文案，不过是因为你，没有你字字珠玑也不足惜
??这场仲夏夜开启的梦，我们陪你一起走到最后吧[爱你]
我以前觉得追星肤浅，认识你之后才知道是我肤浅，陈意涵我爱你
如果生命能够重来，不论几次我都愿意和你相遇。不管你在世界的哪个地方，我一定会，再次去见你的。
那清冷的寒风，因为涵涵你，我身边的所有人都笑的温暖
我不知道你最近好吗？但我知道，我想你的时候，你就会收到思念。
我的思念和我的祈祷，都会换成一点点的幸运，让你一世无忧！
人生自是有情痴，此恨不关风与月。有人如那山间水，纯洁净化暖人心。
人生满满风尘路，无人遮风避雨港。许涵一生平安乐，愿作尘土不羡星。
这一首歌唱给你听我想告诉你，我喜欢你 好多好多的日子里，我一直注视你。
这首歌我唱给我听，也代表我的心情，那样爱你的心情，你是否有一点在意。
遇见你之前每天生活很懒散，遇见你以后，你成为了我努力的动力，让我每一天都向往而生
爱，是把心放在了中间，把你放在了上面，把我放在最低的地方，我爱你，就是这样了吧。
我总在意流云与星群的坐标，一朵花开谢的时日，原野与平川一望无垠是否平展。
哪知你轻轻抬起眉梢，竟赐予我一生大好河山。
你常说意中人是你最大的收获，可是你也是意中人最大的收获啊，你说我们是你的盖世英雄，其实你也是我们的盖世英雄
你是我的玫瑰你是我的花，意中人的情话只给您夸
我愿做你公路上的路标，见证你驶向一个又一个终点就好
难道你不知道吗 自从我第一次看到你 我所走的每一步 都是为了更接近你啊陈意涵
勿忘初心，陈意涵深得我心。
瘦影自怜秋水照，卿须怜我我怜卿。伊人是那天上星，照我心中一轮月。
我也曾把光阴浪费，甚至莽撞到视死如归，只因爱上你，我才渴望长命百岁。
我们是共同存在的，陪你岁岁无忧长长久久，来日方长可期许
.爱是把心放在了中间，把你放在了上面，把我放在最低的地方，我爱你，就是这样了吧。
.喜欢你到整个世界森林里的老虎全部融化成黄油[心]
.我的涵，你是那样的美，美得像一首抒情诗。你全身充溢着少女的纯情和青春的风采。
.希望每晚星亮入梦时，有人来代替我吻你
那天空的乌云，因为涵涵你，我看见了雨后彩虹，从此，不怕风雨。
意涵就是这条街最靓的仔，无论走到哪都是最靓丽的风景线，意涵，我爱你
.天空，大海都是蓝色，都有包容一切的温柔，意中人愿为你包容一切，换你眉欢眼笑
.那清冷的寒风，因为涵涵你，我身着单薄衣裳也不觉冷，从此，心中有阳光。
.人生自是有情痴，此恨不关风与月。一遇我涵误终身，便是西施也黯然
.100种的样子，有100种的美丽，100种喜欢⋯喜欢你的淡定从容，喜欢你内心的笃定坚持，喜欢你现场与粉丝活泼机灵的对话⋯很美好的一个女纸
.那街边的霓虹灯光，因为涵涵你，我看见了人间繁华，从此，不怕闹市烦扰。
.我真的不敢看向陈意涵的眼睛 我怕她眼底的温柔融化了
我不知道你最近好吗？但我知道，我想你的时候，你就会收到思念。
我的思念和我的祈祷，都会换成一点点的幸运，让你一世无忧！
.意中人是深深的大海,而你是那自海的另一边升起的曙光,永远照亮着我们。
你的气息是琐窗朱户的锦瑟，是花落水流红的丝缕杂质，是芳尘余存的袅袅雾霭，是满城风絮的闲愁万种。
无关风月，只得心下了然绽放的烟火，与味甜却生性寒凉的禁果。
.与涵初相识，犹如故人归。与涵再相见，便是金风玉露一相逢，胜却人间无数。
.该说的都说的清楚了，何必掩饰呢.意中人陈意涵，不需要掩饰.
常言道，爱人者，人恒爱之。你爱着人们，也会受到人们的爱。这份爱，不分你我，永恒
.你笑的时候，彻夜未眠的海棠花，湖畔堆烟的杨柳，拂面的风夹裹着的逐水飞絮
凌波不过月台花榭的堇碟，梅子黄时雨，都为你停驻，而后更为跃动的舞上一曲。
希望每晚星亮入梦时，有人来代替我吻你
我看着东边的日出西边的雨，挂念远方的天气和心里的你@
那天空中的你，照耀我心房也是足够温暖
南风过境，春风十里不如你
谢谢你，让平凡的我能够成为另一个人的盖世英雄。
.星星有多美，夜晚会知道。鱼儿有多美，海洋会知道。陈意涵有多美，我想让全世界知道。
春风十里，二十里，三十里，海底两万里，扶摇直上九万里
铁板烤里脊，芝士土豆泥，不如你，都不如你。
.原来盖世英雄也是普通人，但希望给你的温暖，无人能比。希望大闹天宫的日子，不负你
.我不知道你最近好吗？但我知道，我想你的时候，你就会收到思念。我的思念和我的祈祷，都会换成一点点的幸运，让你一世无忧
谢谢意涵的微笑，慌乱过我的年华
.你就像是三棱镜，因为你平凡的阳光也能变成彩虹
喜欢你到整个世界森林里的老虎全部融化成黄油
只缘我涵一回眸，使我思涵朝与暮。除非黄土白骨，我守涵百岁无忧。莫问前程万里远，只管
只管勇往无回头。天若有情天亦老，我若变心我枉生
哪里有什么百万文案，不过是因为你，没有你字字珠玑也不足惜
这场仲夏夜开启的梦，我们陪你一起走到最后吧[爱你]
我以前觉得追星肤浅，认识你之后才知道是我肤浅，陈意涵我爱你
.如果生命能够重来，不论几次我都愿意和你相遇。不管你在世界的哪个地方，我一定会，再次去见你的。
那清冷的寒风，因为涵涵你，我身边的所有人都笑的温暖
.我不知道你最近好吗？但我知道，我想你的时候，你就会收到思念。我的思念和我的祈祷，都会换成一点点的幸运，让你一世无忧！
人生自是有情痴，此恨不关风与月。有人如那山间水，纯洁净化暖人心。
人生满满风尘路，无人遮风避雨港。许涵一生平安乐，愿作尘土不羡星。
.这一首歌唱给你听我想告诉你，我喜欢你 好多好多的日子里，我一直注视你。
这首歌我唱给我听，也代表我的心情，那样爱你的心情，你是否有一点在意。
.遇见你之前每天生活很懒散，遇见你以后，你成为了我努力的动力，让我每一天都向往而生
爱，是把心放在了中间，把你放在了上面，把我放在最低的地方，我爱你，就是这样了吧。
我总在意流云与星群的坐标，一朵花开谢的时日，原野与平川一望无垠是否平展。
哪知你轻轻抬起眉梢，竟赐予我一生大好河山。
.你常说意中人是你最大的收获，可是你也是意中人最大的收获啊，你说我们是你的盖世英雄，其实你也是我们的盖世英雄
你是我的玫瑰你是我的花，意中人的情话只给您夸
.我愿做你公路上的路标，见证你驶向一个又一个终点就好
难道你不知道吗 自从我第一次看到你 我所走的每一步 都是为了更接近你啊陈意涵
.勿忘初心，陈意涵深得我心。
.爱要怎么说出口，我的心里好难受
如果能将你拥有，第一次摸你的手
.、你是我们大家的活宝
你到处散发着诱人的魅力
.没有你，我们今天不会这么圆满
.你给人感觉到一种权威和力量的存在
你让我们越来越有信心
你有有这方面的天赋
你真是一个德高望重的人
你表现这么优秀，和你在一起的时候压力好大啊！
你全身充溢着少女的纯情和青春的风采，真是世间少有。
你也许没有水汪汪亮晶晶的眼睛，但你的眼神也应该顾盼多情，勾魂摄魄。
只有你那嵌着梨涡的笑容，才是我眼中最美的偶象。
你就好像是上品的西湖龙井，那种淡淡的苦涩是你的成熟，越品你越有味道。
你就像那沾满露珠的花瓣，给我的空间带来一室芳香。
你也许没有一簇樱唇两排贝齿，但你的谈吐也应该高雅脱俗，机智过人。
尽管你身材纤弱娇小，说话柔声细气，然而却很有力量，这是一种真正的精神美！
我觉得世界上就只有两种人能吸引人，一种是特漂亮的一种就是你这样的。
你身着一件紫红色旗袍，真像一只美丽的蝴蝶飞过一样，既美丽称身，又色彩柔和。
遇见你之后，再看别的女人，就好象是在侮辱自己的眼睛！
你也许没有若隐若现的酒窝，但你的微笑一定是月闭花羞，鱼沉雁落。
如果我是导演，那么你将是我心目中的最佳的女主角
如果女孩子长得很漂亮，你就夸他：你长得很美。
如果女孩子长得不漂亮，你就夸他：你长得很有气质。
如果女孩子长得即不漂亮又没气质，你就夸他：你长得很可爱。
如果女孩子长得即不漂亮又没气质，又不可爱，你就夸他：你长得很有特点。
如果连特点都没有，你就对她说，你可以跳河了。
看你不再看美女请你不要经常出现在街上好吗？不然交通事故会增加的！
8你的头发真美，尤其那种香味让我心神恍惚，哪是你自己的味道。
你的眼神如此撩人，让我忍不住地去吻她，别动，你会让我越陷越深的。
求你不要再打扮了，给其他的女人留点自信吧，
世上有两种女孩最可爱，一种是漂亮；一种是聪慧，而你是聪明的漂亮女孩。
我好幸运呀，贾宝玉身边有花香袭人的美人，我有眼如水杏般的可爱少女，不比他差，哈哈。
我认为世界上最漂亮的女人是维纳斯，接着就是你！
智慧女人是金子，气质女人是钻石，聪明女人是宝藏，可爱女人是名画
据我考证，你是世界上最大的宝藏，里面装满了金子钻石名画。
在人流中，我一眼就发现了你。我不敢说你是她们中最漂亮的一个，可是我敢说，你是她们中最出色的一个。
瀑布一般的长发，淡雅的连衣裙，标准的瓜子脸，聪明的杏仁眼，那稳重端庄的气质，再调皮的人见了你都会小心翼翼。
智慧女人是金子，气质女人是钻石，聪明女人是宝藏，可爱女人是名画，据我考证，你是世界上最大的宝藏，里面装满了金子钻石名画！
遇见你之后，再看别的女人，就好象在侮辱我自己
你像一片轻柔的云在我眼前飘来飘去，你清丽秀雅的脸上荡漾着春天般美丽的笑容。
你全身充溢着少女的纯情和青春的风采。留给我印象最深的是你那双湖水般清澈的眸
你有点像天上的月亮，也像那闪烁的星星，可惜我不是诗人，否则，当写一万首诗来形容你的美丽。
你也许没有一簇樱唇两排贝齿，但你的谈吐也应该高雅脱俗，机智过人。
你笑起来的样子最为动人，两片薄薄的嘴唇在笑，长长的眼睛在笑，腮上两个陷得很举动的酒窝也在笑。
你娉婷婉约的风姿，娇艳俏丽的容貌，妩媚得体的举止，优雅大方的谈吐，一开始就令我刮目相看。
你也许没有若隐若现的酒窝，但你的微笑一定是月闭花羞，鱼沉雁落。
、你是那样地美，美得象一首抒情诗。
只有莲花才能比得上你的圣洁，只有月亮才能比得上你的冰清。
你那瓜子形的形，那么白净，弯弯的一双眉毛，那么修长；水汪汪的一对眼睛，那么明亮！
你是花丛中的蝴蝶，是百合花中的蓓蕾。无论什么衣服穿到你的身上，总是那么端庄好看。
在你那双又大又亮的眼睛里，我总能捕捉到你的宁静，你的热烈，你的聪颖，你的敏感。
行万里路，读万卷书。
书山有路勤为径，学海无涯苦作舟
、读书破万卷，下笔如有神。
我所学到的任何有价值的知识都是由自学中得来的。——达尔文
少壮不努力，老大徒悲伤。
黑发不知勤学早，白首方悔读书迟。——颜真卿
宝剑锋从磨砺出，梅花香自苦寒来。
读书要三到：心到、眼到、口到
玉不琢、不成器，人不学、不知义。
一日无书，百事荒废。——陈寿
书是人类进步的阶梯。
一日不读口生，一日不写手生。
我扑在书上，就像饥饿的人扑在面包上。——高尔基
书到用时方恨少、事非经过不知难。——陆游
读一本好书，就如同和一个高尚的人在交谈——歌德
读一切好书，就是和许多高尚的人谈话。——笛卡儿
学习永远不晚。——高尔基
少而好学，如日出之阳；壮而好学，如日中之光；志而好学，如炳烛之光。——刘向
学而不思则惘，思而不学则殆。——孔子
读书给人以快乐、给人以光彩、给人以才干。——培根
敏而好学，不耻下问——孔子
业精于勤，荒于嬉；行成于思，毁于随——韩愈
学而不思则罔，思而不学则殆——孔子
知之者不如好之者，好之者不如乐之者——孔子
三人行，必有我师也。择其善者而从之，其不善者而改之——孔子
兴于《诗》，立于礼，成于乐——孔子
己所不欲，勿施于人——孔子
读书破万卷，下笔如有神——杜甫
读书有三到，谓心到，眼到，口到——朱熹
立身以立学为先，立学以读书为本——欧阳修
读万卷书，行万里路——刘彝
黑发不知勤学早，白发方悔读书迟——颜真卿
书卷多情似故人，晨昏忧乐每相亲——于谦
书犹药也，善读之可以医愚——刘向
少壮不努力，老大徒伤悲——《汉乐府。长歌行》
莫等闲，白了少年头，空悲切——岳飞
发奋识遍天下字，立志读尽人间书——苏轼
鸟欲高飞先振翅，人求上进先读书——李苦禅
立志宜思真品格，读书须尽苦功夫——阮元
非淡泊无以明志，非宁静无以致远——诸葛亮
勿以恶小而为之，勿以善小而不为——陈寿《三国志》
熟读唐诗三百首，不会作诗也会吟——孙洙《唐诗三百首序》
书到用时方恨少，事非经过不知难——陆游
问渠那得清如许，为有源头活水来——朱熹
旧书不厌百回读，熟读精思子自知——苏轼
书痴者文必工，艺痴者技必良——蒲松龄
读书百遍，其义自见——《三国志》
千里之行，始于足下——老子
路漫漫其修道远，吾将上下而求索——屈原
奇文共欣赏，疑义相如析——陶渊明
读书之法，在循序而渐进，熟读而精思——朱熹
吾生也有涯，而知也无涯——庄子
非学无以广才，非志无以成学——诸葛亮
玉不啄，不成器；人不学，不知义——《礼记赞扬，
像黄金钻石，只因稀少而有价值。 ——塞缪尔·约翰逊
称赞不但对人的感情，而且对人的理智也起着很大的作用。 ——列夫·托尔斯泰【俄】
人生的价值，应当看他贡献什么，而不应当看他取得什么。 人生的价值，并不是用时间，而是用深度去衡量的
人的价值是由自己决定的。 －－ 卢梭
自己活着，就是为了使别人活得更美好。－－雷锋
要有积极的人生态度，不要受了点挫折就想不开，人生最尊贵者莫过于生。——方海权
一个人做点好事并不难，难的是一辈子做好事，不做坏事。-- 毛泽东
不飞则已,一飞冲天;不鸣则已,一鸣惊人。
莫明的我就喜欢你，自从认识你起，你的一举一动就深深的在我的每一个细胞里。等你爱我。
你在的时候，你是一切；你不在的时候，一切是你。吾爱永恒！
宝贝我爱你，我不在的时候照顾好自己；无论有多远，我一定要回来和你在一起。
爱你就是爱自己，爱自己就是爱你~~~因为你我本是一体
总想拥有你的一切，或许我是为你而也生。也许我也是为了你而死
我爱你就象你爱我一样，我心中的你就象你心中的我一样，我爱你的方式就象你爱我的一样。
我是真的爱你永远的永恒的
世界上最遥远的距离，不是天个一方，也不是生死之间，而是我就在你身边你却不知道我爱你！
窗外月光如水，我的心也如水，但如钱塘江大潮般汹涌不绝！
不要忘了我们一起走过的桥！
我时刻在想你，没有你我吃不下饭，睡不好觉，你在哪里！！
等到一切都看透，希望你陪我看细水常流！
你知道第一次，你给我的感觉，让我不知不觉得爱上了你，爱给了我⋯⋯不，是你给了我那初恋触电的感觉
投入需要勇气，可一旦投入很难回头。好好工作，好好想我，不要没有信息，不要没有思念。
思念就像巧克力，苦苦的，甜甜的⋯⋯不敢想你，怕会想你：不敢说想你，怕更想你⋯⋯其实，我真的真的好想你！
你走了，在我心里丢下一颗种子，我用孤独灌溉它，终于它发芽了。开花，结果，几乎一瞬间，我将果实剥开，发现果核上刻着“颖，我爱你”
空间的差距不会让我们疏远，时间的考验我们可以一起一起度过，还是那两个字--等我
每时每刻在看着你我总觉得看不够，天天呆在一起我还觉得呆不够，总想把你搂在怀，将你融化在我的爱里
爱你让我心痛，我也许执着，只是那种执着很美，也很悲壮！
看到周围的每一个角落，都有你与我的故事，慢慢品尝我们之间的爱与恨。我想你给我一个
爱是多么神奇，它能让我如此陶醉，不能自制！爱他是多么幸福，他让我如痴如醉，不能自拔！
我不知道如何才能表达我对你的那分情，我只知道没有你我会憔悴到死，就象那朵凋谢的玫瑰一样，失去灵魂！
没有你的城市，我就像一个没有爱情温暖的男人；很想你的时候，我就静静轻轻呼唤你的名字。我爱你！这是我一生的承诺
我爱你就像老鼠爱大米，我泡你就像方便面泡在水里，但俺还是喜欢你！
一个人一生真爱只有一次，只有一人。
这一生有了你，就算有再大的风雨，再大的不如意，我都要和你走过每一个春夏秋冬，我爱你
我会好好珍惜你的，我的亲亲！以后的风雨人生路，我愿陪你一同走过
也许是今生有缘，让我在最无助的遇到了你，是你给了我幸福的感觉。
我爱你，没有理由！请记住：我时刻都在想你。记住我的吻
也许今生我们将无法相依相伴，心灵却永远相通。你是我今生的最爱，也是我今生的永恒！
你是树儿，我是滕，我会缠着你一辈子。我会陪你坐着摇椅慢慢变老！
我总是在呼吸的时候想你，所以我时时刻刻想念你
爱你爱的值得，错的值得，是执着是洒脱留给别人去说，为爱身陷的我，只有为你才会那么做！
我会永远爱你，一生一世，爱你永不变⋯⋯
很爱很爱你所以愿意舍得为你！往幸福自由的地方飞去
颤颤思音，能兑现你一缕青丝吗？你的案，请放在你的呼吸里让我梦见。
唤你一声“亲爱的”，在深夜凸现，在心间永恒。
就算整个世界都抛弃了我，我还是会一如既往的爱着你，永远
我虽然不能活一百岁，但我却要说，我会爱你一万年，我会用我的身心爱你、疼你、想你、念你在每一个黑夜和白天！！！
本想给你一丝春风，却给了你整个春天；
不要让我们渡过一个没有彼此的情人节⋯忘了过去吧，我爱你
相识在于有缘，相知在于有心，相惜贵于友情，相知、相惜的日子，我愿意，陪你一起走过。
当你不在我身边，才蓦然发觉你之于我的重要性。没有你的夜真的好寂寞，好漫长。每天想你一百遍，每一次想念都让我沉醉
在一年的每个日子，在一天每个小时，在一小时的每一分钟，在一分钟的每一秒，我都在想你。
当我遇上你，使我相信你是我的唯一，只可惜天意弄人让我们分隔两地，到底我们什么时候才能在一齐共筑爱巢呢
我今生今世爱定你！愿这一生只牵你的手！
我并不痴情，可我回守侯你一生； 我不是弱智，但我会傻傻的爱你--到永远！
我将把你紧紧地搂在怀中，吻你亿万次，像在赤道上面那样炽烈的吻
爱不需要理由，但生活需要理由，生活让我离开你，爱就让它深埋心底！
你说本善良，只缘事伤人，真想六根清，但恨无情人，欲把山河动，只叫世人醒。
这样的习惯也是一种甜蜜的负担，思念你早已成为我生活中不可缺少的习惯
想着，某天与你在细雨中静静地散步。让雨点敲打着心扉，在这轻灵的世界里感受彼此那份真实的回音⋯⋯
虽然你没有出众的外表，但你的成熟魅力无人能比；虽然你缺乏浪漫的温情，但你的体贴令我心驰神往
保留一个最浪漫的故事，给你一声祝福，一个kiss，爱你直到永远！！！
爱一个人需要勇气，因为他需要一生的守候。
你的烦恼我来承担，我的快乐你来分享。
爱你的感觉，永远都是那么美；你那温柔的笑脸；是我致命的弱点；爱你爱你⋯⋯不管今生或来世，我将永远爱你。
没有理由，没有原因，我就是爱你，爱你，永远爱你，让我们将爱情进行到底！
爱情是一朵带刺的玫瑰花，扎到了，会痛会流血，希望我们把握好我们心中那份小小的爱！
为什么我的眼里常含泪水，因为我对你爱得深沉。
一些路我们并肩走过，一些故事我们就是主人公，一首歌我们对唱了那幺久，永远不变的是心中深藏的对爱的执着
分开的一分一秒使我明白，男人的心也是玻璃做的；想你的每时每刻让我懂得，我的心也需要爱的抚慰。
遇见你是个错，爱上你是一错再错，离开你是错上加错。
因为不知来生来世会不会遇到你，所以今生今世我会加倍爱你。
在这世纪第一个情人节，祝你情人节快乐。
我越来越喜欢你了。
我今生最大的奢望就是：天天和你在同个盆里洗脚。平淡相守到老--老到我们哪也去不了
如果有一天你有了大肚腩，我依然会为你做晚餐！
我们，就是一张纸的两面，如何才能分开呢？
想你在每一刻。爱你在每一天
有你的日子你是一切，没你的日子一切是你
是鬼迷了心窍也好，是上天的注定也好。总之能够认识你是我这一生最大的快乐。
我将把你紧紧地搂在怀中，吻你亿万次，像在赤道上面那样炽烈的吻
注意身体！知道吗？我最不希望的就是看到你生病！真的！
如果爱你是错的话，我不想对；如果对是等于没有你的话，我宁愿错一辈子；如果非要把着份爱加上一个期限，我希望是一万年！！！
不同的时间，不同的地点，不同的人群，相同的只有你和我；时间在变，空间在变，不变的只有对你无限的思念！
你是疯子我是傻，二半吊子少半啦，没有你就不疯来，少了我也就不在傻，你在哪来我在哪，你要死了就少俩
对你的思念是一天又一天，美丽的梦何时才能出现，亲爱的：好想再见一面
寒夜里，冷冷的，举起手，呵了一口气，让我想起了你的手，那只需要我温暖的手，想告诉你，你已经是我的一部分
读你之后才读会美；懂你之后才懂得爱。我识美，所以为你沉醉；我懂爱，所以千缘难再！
你问我，我有多爱你。我无法回答，因为你得先告诉我，你的一生有多长
当清风吹起我的长发，我独自一个人站在山顶，好寂寞，只为等待苦苦思念的远方的人儿
想你已成为习惯，爱你已是我生活的一部分，
我愿我们能够变成蝴蝶，哪怕只在夏季里生存3天也就够了，我在这3天中所得到的快乐要比平常50年间所获得的快乐多得多
没有你的日子里，我会更加珍惜自已。
人总是会老的，希望到时，你仍在我身边有你相伴的日子，即使平凡也浪漫！
我得到了一个完美的你，一个真实的你，一个无以伦比的你，一个要把我全身心的爱倾诉的你！
如今我已经记不清，曾经多少次和你一起走在海滩上了。但我相信，那亘古不变的海风海浪会记得我俩的每一个絮语晨昏
你好吗？你不要在生气了如果你还不开心你就找我来好吗？我想对你说我真的很爱你真的？
心里，有时很大，可以用来撑船，但对于你和我，又好小好小，因为那里只有我和你，不是吗？
你是我心目中百分之一百的女孩！如果真的可以，我愿意和你一生相伴！但是
你快乐所以我快乐，你痛苦所以我难受
千言万语也表达不了我对你的感情，我只想与你一同走过。
当我的笑容在等待中慢慢变成泪水，我想我该离开你了。然而，我还在爱里停留
如果你需要我爱你亿万年，我回陪你到天荒地老！对不起，我爱你！！！
爱上你是我一生最大的痛，痛在不能分分秒秒的拥有你！
爱你不是把你放在嘴上，我把你藏在心里，为你好好过每一天，把你珍藏到永远！
如果一切重新来过，如果结局还是这样，一段没有结果的感情，我还是会选择爱你，不会后悔。
想你是我唯一可做的事，爱你是我唯一可走的路！
你走了那么久，我希望你一点都没有变，就像我对你的爱，走再久，也依旧！
我愿做天上的星星，给你永恒的光芒，永远守候在你身边
我能想到最浪漫的事，就是和你一起慢慢变老，直到我们老的哪儿也去不了，你还依然把我当成手心里的宝。
我要你做世界上第二幸福的人，你会问：为什么不是第一，因为让我认识到你，我就是世界上最幸福的人
无论我们相隔多远，我心与你心始终相牵！！
有你的日子我度年如日，没有你的日子我度日如年。
、老婆老婆我爱你就像老鼠爱大米！！！！不打你不骂你就用感情折磨你！！！！！
在情人节的那天夜里，我想听到的话是我爱你，我希望你做的事是，抱着我，靠着我，说爱我。
一句平淡的话：知不知道，你很重要。
有一种声音是听不见的，有一种语言是不能亵渎的，有一种感觉是无法描述的，有一种力量是不可抗拒的
想见你，没有你，闭上眼，晃动的全都是你，我的心，其实从来不曾离去，这一生只想和你在一起，全世界最重要的是你
如果爱你是错的话，我不想对；如果对是等于没有你的话，我宁愿错一辈子；如果非要把着份爱加上一个期限，我希望是一万年
有一天世界只有一份爱，那一定是我对你的。
时间在你我相聚的时候是如此的短暂，多想在那一刻时间就此停住，让你我拉着的手永不分离。
有你的日子，我的生活多了一份温馨和快乐。
山无棱，天地合，才敢与君绝
你是我永远的情人，愿今后的每一个情人节都有我在你身边。我没有浪漫的词汇，但我可以给你真实的爱。
情人节到了，让我们共同祝愿：我们的爱情地久天长；我们永远相依相伴，相爱到老！
、佛说：前世的五百次回眸，才换来今生的擦肩而过。我用一万次换来与你的相遇，希望能亲口告诉你：“永远永远爱你”。
请将昨日的痛苦变成一场恶梦，忘了它。请将今天的快乐变成一段回忆，珍藏它。请将明朝的憧憬变成一种动力，追随它。
回想我们在一起相聚的日子，我的心绪迷迷朦朦。你那充满朝气的身躯总是伴着月光入我梦来，让我牵挂不停
我不是不想见你，而是因为我怕破坏我们之间的那份神秘感！！
因为有你，我的世界才会如此完美，爱你是我唯一的理由！ I LOVE YOU! 吻你！每夜枕着你的名字入睡
、生活因你而改变，人生因你而改变，情绪因你而改变，不变的是我爱你。
一见钟情是你我的缘份，距离却是你我的阻碍。你我之间能否演预出一场动人的童话？我期待着美丽的结局。
在你离开的那一刻已开始想你
、因为有你让我掀起一片爱的涟漪！
当每个人都以不屑的眼光冷漠你的时候，别忘了，我在乎你
不需要太多，只要你抛开一切，说一句我爱你。我等的太久了，感觉好累好累。但⋯⋯我等你。
生活给我出了个难题，送给我这么可爱的你，我该怎么庆祝？生活也给你出了个难题，送给你这么忠诚的我，你该如何解决？
见到你不想你，想你又见不到！
请相信我，爱你。
、但愿你的眼睛，只看得到笑容，但愿你流下每一滴泪，都让人感动，但愿你以后每一场梦，不再一场空
被爱是很幸福的，但我愿你幸福一生
当众人的都注视着那位漂亮迷人的美女的时候，别忘了，我在看你
不敢说我会等你一辈子，因为我没有几个四年可以去耗费。但相信我会爱你一辈子，因为你给我的没有人能再给我。
我的梦中情人，她有一头像你一样乌黑亮丽的秀发。
我爱你是忠于理想，忠于自己的选择。
但愿你的眼睛，只看得到笑容，但愿你流下每一滴泪，都让人感动，但愿你以后每一场梦，都让人感动
任何华丽的言语都不及这三个字：“我爱你！”
、亲爱的多保重身体，要知道远方的我在时刻惦记着你，爱我就要好好爱惜你自己！爱你的田田
我可不可以向你预约明年的情人节。如果可能的话，有生之年的情人节都和我一起渡过好吗？情人节快乐。
每一天都在变，不变的是我对你的感情和一颗永远爱你的心
"""

all_talks = all_talks.split("\n")
all_talks_count = len(all_talks)
all_talks = all_talks[1:all_talks_count-1]



titles = u"""
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#做你的意中人
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#涵仔加油
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#涵涵冲啊啊啊啊
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#我爱你涵涵
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#涵涵你好美
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#大家doki加油啊啊啊
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#做你的盖世英雄
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#涵涵生日快乐
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#从来没有想到会遇见你
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#你是上天最好的礼物
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#数据第一意涵第二
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#我也曾把光阴浪费
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#美得像一首抒情诗
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#意涵就是这条街最靓的仔
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#我们陪你一起走到最后
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#慌乱过我的年华
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#谢谢意涵的微笑
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#一睁眼便看见你在笑
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#不如你，都不如你
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#一个人的盖世英雄
【陈意涵】#陈意涵这就是灌篮# #陈意涵1017生日快乐#春风十里不如你
【陈意涵】[心]这场仲夏夜开启的梦，我们陪你一起走到最后吧[爱你]
【陈意涵】谢谢意涵的微笑，慌乱过我的年华
【陈意涵】哪有什么岁月静好，不过是一睁眼便看见你在笑罢了
【陈意涵】谢谢你，让平凡的我能够成为另一个人的盖世英雄。
【陈意涵】南风过境，春风十里不如你[心]
【陈意涵】[心]有你的地方，就是心动现场[米奇比心]
【陈意涵】万物复苏，春暖花开，都是因为你的出现。
【陈意涵】意涵就是这条街最靓的仔，无论走到哪都是最靓丽的风景线，意涵，我爱你
【陈意涵】难道你不知道吗自从我第一次看到你我所走的每一步都是为了更接近你啊陈意涵
【陈意涵】我做不来好人，也不敢做坏人，只想做你的意中人。
【陈意涵】你是我的玫瑰你是我的花，意中人的情话只给您夸[doge]
【陈意涵】我以前觉得追星肤浅，认识你之后才知道是我肤浅，陈意涵我爱你??
【陈意涵】哪里有什么百万文案，不过是因为你，没有你字字珠玑也不足惜
【陈意涵】你就像是三棱镜，因为你平凡的阳光也能变成彩虹
【陈意涵】不太冷的寒冬，盛夏夜的风，繁星点缀的天空和每个有你的梦
【陈意涵】我愿做你公路上的路标，见证你驶向一个又一个终点就好
【陈意涵】我看着东边的日出西边的雨，挂念远方的天气和心里的你
【陈意涵】该说的都说的清楚了，何必掩饰呢.意中人??陈意涵，不需要掩饰.
【陈意涵】我还是很喜欢你，就像星辰倾泻，月光与血。愿你万事胜意，闪耀星空。
【陈意涵】因为有你，终于让我的生命有了一点点的不一样。[心]
【陈意涵】[心]今夕何夕，见此佳人。涵非凡间等闲辈，是那仙女下凡来。
【陈意涵】与涵初相识，犹如故人归。与涵再相见，便是金风玉露一相逢，胜却人间无数。
【陈意涵】[心][心]春水初生，春林初盛，春风十里，不如一个陈意涵。
【陈意涵】等闲易变常人心，唯有故人心不变。即是意中人才俊，一心一意守一涵。
【陈意涵】情不知所起，一往而深，生者可以死，死者可以生。唯独此情，永世不灭
【陈意涵】瘦影自怜秋水照，卿须怜我我怜卿。伊人是那天上星，照我心中一轮月。
【陈意涵】我把平生卷起，星辰摘下，恰似你一瞥一笑直穿心房
【陈意涵】意下有一心，涵中纳三川。百川纳海不及一心陈情[心]
【陈意涵】踏花而去，留一世独白，叹一生无奈，只为与你相知而遇。
【陈意涵】一颦一笑使人醉，一生一世意中人[心]
【陈意涵】相思树底说相思，思涵念涵你可知？[害羞]
【陈意涵】若教美中无意涵，不信人间有仙女。直道伊人天上有，未妨恋她至白头。
【陈意涵】重温旧梦赏涵字，人生乐趣亦无忧。不关人间风与月，我守意涵终一生
【陈意涵】逍遥人间游戏王，一颦一笑皆动心。不喜人生诸多事，唯独恋这美人心。
【陈意涵】莫道不消魂，只因未遇她。一见倾城笑，回眸误众生
【陈意涵】认识你之前，山是山，海是海，认识你之后，山海都是你[太开心]
【陈意涵】你见山川多清秀，星辰多温柔，恰似你眼眸
【陈意涵】你笑起来的时候，天空都变了颜色，粉红色。
【陈意涵】你是大千世界一汪清泉，愿那些风马牛与你永不相及。永随你，去哪??
【陈意涵】我喜欢穿过窗帘缝隙的阳光喜欢清凉秋日的晚风还喜欢有你存在的每一个年月
【陈意涵】任百花无数，我只摘一朵；任弱水三千，我只取一瓢；任群芳百艳，我只在乎你
【陈意涵】人活着，不能没有方向。谢谢我的涵涵，给了我活着的方向~与你一起进步
【陈意涵】腹有诗书气自华，所以有才的你气质真的与众不同。
【陈意涵】只要是你开车，无论是玛莎拉蒂还是拖拉机，我们都喜欢
【陈意涵】你笑，意中人的心就化了，你哭，意中人的心就碎了
【陈意涵】爱你就像x=0，y=0，一条直线，不会转弯
【陈意涵】多希望能学会分身术，哪有就有千千万万个我可以保护你。
【陈意涵】不管我去哪，我最想留在你身边。
【陈意涵】人间不值得，而陈意涵值得[米奇比心]
【陈意涵】孙悟空的月光宝盒为紫霞仙子打开，意中人的爆炸盒子为意涵仙女而做
【陈意涵】赠人玫瑰，手有余香。爱涵一生，爱有回音
【陈意涵】我对感情很挑剔，只对你有感觉
【陈意涵】话唠的原因还不是因为太喜欢你了
【陈意涵】你从一个陌生人，变成了一个我最舍不得离开的人
【陈意涵】一首诗词天涯路，始信人间有真爱。涵若幸福福安康，我替人间许平安。
【陈意涵】风筝为什么飞得高，因为地上有人蹒跚奔跑。我愿意做那个奔跑的人
【陈意涵】那世人眼里的功名利禄，因为涵涵你，我风轻云淡，从此，为爱而生。
【陈意涵】喜欢一切可爱的人与事，喜欢世间外物，但我更喜欢你，因为你是可爱本身。
【陈意涵】月色真美，就和你一样
【陈意涵】你可以是一杯牛奶温暖我的胃，也可以是一杯酒光是香味就让我沉醉
【陈意涵】上天帮你造就了一双巧手，第一次见面，就偷偷偷走我的心。
【陈意涵】我真的不敢看向陈意涵的眼睛我怕她眼底的温柔融化了我
【陈意涵】那清冷的寒风，因为涵涵你，我身着单薄衣裳也不觉冷，从此，心中有阳光。
【陈意涵】那街边的霓虹灯光，因为涵涵你，我看见了人间繁华，从此，不怕闹市烦扰。
【陈意涵】那天空的乌云，因为涵涵你，我看见了雨后彩虹，从此，不怕风雨。
【陈意涵】希望每晚星亮入梦时，有人来代替我吻你
【陈意涵】喜欢你到整个世界森林里的老虎全部融化成黄油[心]
"""

titles = titles.split("\n")
count = len(titles)
titles = titles[1:count-1]





home_url='https://v.qq.com/x/star/1661556?tabid=3'
post_url='https://v.qq.com/doki/doki_note/new?starid=1661556&dataKey=starid%3D1661556%26ftid%3D51661556%26targetid%3D2657077965'



def pc_url(url):
	if "http://m.v.qq.com/x/bar/post/detail_h5.html" in url:
		url = url.split("=")[1]
		url = url.split("&")[0]
		url = "https://v.qq.com/doki/doki_note/detail?starid=1661556&noteid=" + url + "&dataKey=starid%3D1661556%26ftid%3D51661556%26targetid%3D2657077965\n"
	return url

def is_login(driver):
	try:
		return driver.find_element_by_xpath("//a[@id='mod_head_notice_trigger']/img").get_attribute("src") != "https://i.gtimg.cn/qqlive/images/20150608/avatar.png"
	except:
		return False


## add class for login

class dokiLogin(object):
    def __init__(self, object):
        self.home_url = 'https://v.qq.com/x/star/1661556?tabid=3'
        ## self.driver = webdriver.Chrome(executable_path = os.getcwd() + '/chromedriver')
        self.driver = object.tab2_driver
        self.to_continue = False
        self.frozen_count = 0

    def get_account_info(self, filename):
        try:
            f = open(filename, 'r')
            accounts = {}
            for line in f:
                user, pw = line.strip().split('----')
                accounts[user] = pw
            return accounts
        except Exception:
            print("获取帐号失败！")

    def is_login(self):
        try:
            self.driver.switch_to.default_content()
            time.sleep(0.5)
            return self.driver.find_element_by_xpath("//a[@id='mod_head_notice_trigger']/img").get_attribute("src") != "https://i.gtimg.cn/qqlive/images/20150608/avatar.png"
        except:
            return False


    def download_images(self, bg):
        bg_url = bg.get_attribute("src")
        fullbg_url = "https://hy.captcha.qq.com/hycdn_0" + bg_url.split("https://hy.captcha.qq.com/hycdn_1")[1]
        if not os.path.exists('Image'):
            os.mkdir('Image')
        urlretrieve(url=fullbg_url, filename='Image/fullbg.jpg')
        #print('原始背景图片下载完成！')
        urlretrieve(url=bg_url, filename='Image/bg.jpg')
        #print('背景图片下载完成！')

    def is_px_equal(self, img1, img2, x, y):
        pix1 = img1.load()[x,y]
        pix2 = img2.load()[x,y]
        threshold = 60
        if abs(pix1[0]-pix2[0]) < threshold and abs(pix1[1]-pix2[1]) < threshold and abs(pix1[2]-pix2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        left = 300
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_px_equal(img1, img2, i, j):
                    left = i
                    return left
        return left

    def cal_dist(self, bg):
        im1 = Image.open('Image/fullbg.jpg')
        im2 = Image.open('Image/bg.jpg')
        scale = bg.size.get("width")/im2.size[0]
        distance = (self.get_gap(im1, im2) * 1 * scale) - 12
        return distance

    def get_track(self, distance):
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 2 / 5
        mid2 = distance * 3 / 4
        # 时间间隔
        t = 0.2
        # 初始速度
        v = 0

        while current < distance:
            if current < mid:
                a = random.uniform(10, 12)
            elif current < mid2:
                a = random.uniform(1, 2)
            else:
                a = -(random.uniform(12.5, 13.5))
            v0 = v
            v = v0 + a * t
            x = v0 * t + 1 / 2 * a * t * t
            current += x

            if 0.6 < current - distance < 1:
                x = x - 0.53
                tracks.append(round(2*x, 2))

            elif 1 < current - distance < 1.5:
                x = x - 1.4
                tracks.append(round(2*x, 2))
            elif 1.5 < current - distance < 3:
                x = x - 1.8
                tracks.append(round(2*x, 2))
            elif 3 < current - distance < 5:
                x = x - 4
                tracks.append(round(2*x, 2))
            elif 5 < current - distance < 7:
                x = x - 6
                tracks.append(round(2*x, 2))
            else:
                tracks.append(round(2*x, 2))

        return tracks



    def captcha_check(self):
        self.driver.switch_to.default_content()
        time.sleep(0.5)
        self.driver.switch_to.frame("_login_frame_quick_")
        time.sleep(0.5)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        time.sleep(1)
        bg = self.driver.find_element_by_id("slideBkg")
        self.download_images(bg)

        distance = self.cal_dist(bg)
        slider = self.driver.find_element_by_id("tcaptcha_drag_button")
        tracks = self.get_track(distance/2)

        times = 0
        while times < 3:
            time.sleep(0.5)
            action = ActionChains(self.driver)
            action.click_and_hold(slider).perform()
            action.reset_actions()

            for x in tracks:
                action.move_by_offset(xoffset=x,yoffset=-0.2).perform()
                action.reset_actions()
            time.sleep(0.5)
            action.release().perform()
            time.sleep(2)

            try:
                alert = self.driver.find_element_by_class_name('tcaptcha-title').text
            except Exception as e:
                alert = ''
            if alert:
                #print('滑块位移需要调整：%s' % alert)
                distance -= 2
                times += 1
                time.sleep(1)
            else:
                #print('滑块验证通过')
                return True

        if times == 3:
            #print("验证码尝试不成功")
            return False


    def check_frozen(self):
        self.driver.switch_to.default_content()
        time.sleep(1)
        self.driver.switch_to.frame("_login_frame_quick_")
        time.sleep(0.5)
        try:
            self.driver.find_element_by_link_text("点击这里")
            return True
        except Exception:
            return False

    def frame_relogin(self, user, pw):
        self.driver.switch_to.default_content()
        time.sleep(1)
        self.driver.switch_to.frame("_login_frame_quick_")
        time.sleep(0.5)
        # self.driver.find_element_by_id("u").clear()
        # time.sleep(1)
        # self.driver.find_element_by_id("u").send_keys(user)
        # time.sleep(1)
        # self.driver.find_element_by_id("p").clear()
        # time.sleep(1)
        self.driver.find_element_by_id("p").send_keys(pw)
        time.sleep(0.5)
        self.driver.find_element_by_id("login_button").click()
        time.sleep(1)
        try:
            if self.is_login():
                #print("帐号" + str(user) + "已成功登录！")
                self.to_continue = True
                return True
            else:
                if self.check_frozen():
                    self.write_frozen_account(user, pw)
                    #print("帐号" + str(user) + "已被冻结！\n")
                    self.driver.delete_all_cookies()
                    self.driver.get(home_url)
                    return True
                else:
                    if self.captcha_check():
                        if self.is_login():
                            #print("帐号" + str(user) + "已成功登录！")
                            self.to_continue = True
                            return True
                        else:
                            return False
                    else:
                        return False
        except Exception:
            return False

    # def check_captcha_tab(self):
    #     try:
    #         self.driver.switch_to.frame("_login_frame_quick_")
    #         time.sleep(0.5)
    #         self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
    #         return True
    #     except Exception:
    #         print("暂时无法登录")
    #         return False


    def login(self, user, pw):
        if self.is_login():
            #print("已登录")
            self.to_continue = True
            return True
        else:
            self.driver.find_element_by_id("mod_head_notice_trigger").click()
            self.driver.find_element_by_class_name("_login_type_item").click()
            self.driver.switch_to.frame("_login_frame_quick_")
            time.sleep(0.5)
            self.driver.find_element_by_link_text('帐号密码登录').click()
            time.sleep(0.5)
            self.driver.find_element_by_id("u").send_keys(user)
            time.sleep(1)
            self.driver.find_element_by_id("p").send_keys(pw)
            time.sleep(1)
            self.driver.find_element_by_id("login_button").click()
            time.sleep(1)
            if self.is_login():
                #print("帐号" + str(user) + "已成功登录！")
                self.to_continue = True
                return True
            else:
                if self.check_frozen():
                    self.write_frozen_account(user, pw)
                    #print("帐号" + str(user) + "已被冻结！\n")
                    self.driver.delete_all_cookies()
                    self.driver.get(home_url)
                    return True
                else:
                    try:
                        if self.captcha_check():
                            if self.is_login():
                                #print("帐号" + str(user) + "已成功登录！")
                                self.to_continue = True
                                return True
                            else:
                                if self.check_frozen():
                                    self.write_frozen_account(user, pw)
                                    #print("帐号" + str(user) + "已被冻结！\n")
                                    self.driver.delete_all_cookies()
                                    self.driver.get(home_url)
                                    return True
                                return False
                        else:
                            return False
                    except Exception:
                        #print("需重新尝试")
                        return False

    def write_failed_account(self, user, pw):
        try:
            failed_account = open(u'密码错误帐号.txt', 'a+')
            failed_account.write(str(user) + "----" + str(pw))
            failed_account.write("\n")
            failed_account.close()
        except Exception:
            print("导出密码错误帐号失败")

    def write_frozen_account(self, user, pw):
        try:
            frozen_account = open(u'冻结帐号.txt', 'a+')
            frozen_account.write(str(user) + "----" + str(pw))
            frozen_account.write("\n")
            frozen_account.close()
            self.frozen_count += 1
        except Exception:
            print("导出冻结帐号失败")

    def write_success_account(self, user, pw):
        try:
            success_account = open(u'成功登录帐号.txt', 'a+')
            success_account.write(str(user) + "----" + str(pw))
            success_account.write("\n")
            success_account.close()
        except Exception:
            print("导出成功登录帐号失败")


class ApplicationUI():

	def __init__(self):
		self.root = tk.Tk()
		self.root.title("涵仔的Doki工具包")
		self.root.update()
		self.root.resizable(False, False) ## 禁止改变界面大小
		# 以下方法用来计算并设置窗体显示时，在屏幕中心居中
		curWidth = self.root.winfo_width()  # get current width
		curHeight = self.root.winfo_height()  # get current height
		scnWidth, scnHeight = self.root.maxsize()  # get screen width and height
		tmpcnf = '+%d+%d' % ((scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
		self.root.geometry(tmpcnf)
		self.setup_UI()		## 创建界面


		self.queue = queue.Queue()
		self.root.after(1000, self.listen_for_result)
		self.root.mainloop()


	def listen_for_result(self):
		self.tab1_loop_time = self.tab1_loop_time + 1
		self.root.after(1000, self.listen_for_result)
		if self.tab1_timing == True:
			self.tab1_now_time = self.tab1_now_time + 1
			self.tab1_sum_time = self.tab1_sum_time + 1
			self.tab1_sum_time_text.set("总计用时：{}秒".format(self.tab1_sum_time))
			self.tab1_now_time_text.set("当前账号用时：{}秒".format(self.tab1_now_time))
		if self.tab2_timing == True:
			self.tab2_now_time = self.tab2_now_time + 1
			self.tab2_sum_time = self.tab2_sum_time + 1
			self.tab2_sum_time_text.set("总计用时：{}秒".format(self.tab2_sum_time))
			self.tab2_now_time_text.set("该组账号用时：{}秒".format(self.tab2_now_time))
		notice = ""
		try:
			 notice = self.queue.get(False)
		except:
			pass
		else:

			if notice == "tab1_stop":
				str = "该账号已刷完，请切换账号！！！\n总计用时：{}秒，当前账号用时：{}秒\n总计刷了{}条评论，当前账号刷了{}条评论！".format(self.tab1_sum_time, self.tab1_now_time, self.tab1_sum_count, self.tab1_now_count)
				tkinter.messagebox.showinfo('温馨提示',str)
				self.tab1_now_time = 0
			elif notice == "tab2_stop":
				str = "该组{}个账号已刷完！用时：{}秒\n成功帐号{}个，密码错误帐号{}个，冻结帐号{}个！" \
                .format(self.tab2_sum_count_account, self.tab2_sum_time, self.tab2_success_count_account, self.tab2_failed_count_account, self.tab2_frozen_count_account)
				tkinter.messagebox.showinfo('温馨提示',str)
				self.tab2_now_time = 0
			elif notice == "tab3_stop":
				str = "转化完成，一共转化{}个链接，评论数小于{}的有{}条".format(len(self.tab3_urls),self.tab3_count,self.tab3_visable_text.get().split(":")[1][0:-1])
				tkinter.messagebox.showinfo('温馨提示',str)
			elif "tab1_error" in notice:
				str = "此软件为意涵专属，请勿盗用！！！\n" + notice.split(",,")[1]
				tkinter.messagebox.showerror("警告",str)

	def setup_UI(self):
		#创建菜单栏
		menu = Menu(self.root)

		#创建二级菜单
		talk_menu = Menu(menu,tearoff=0)
		talk_menu.add_command(label="选择链接文本",command=self.tab1_open_link)
		talk_menu.add_command(label="选择评论话术",command=self.tab1_open_talk)

		send_menu = Menu(menu,tearoff=0)
		# send_menu.add_command(label="选择链接文本",command=self.tab2_open_link)
		send_menu.add_command(label="选择评论话术",command=self.tab2_open_talk)

		about_menu = Menu(menu,tearoff=0)
		about_menu.add_command(label="为了涵涵秃头！！！")

		author_menu = Menu(menu,tearoff=0)
		author_menu.add_command(label="@AskeyNil：完成基本功能，GUI界面搭建")
		author_menu.add_command(label="@一棵木鱼：完成自动登录部分验证码识别")


		#在菜单栏中添加以下一级菜单
		menu.add_cascade(label="评论",menu=talk_menu)
		menu.add_cascade(label="发帖",menu=send_menu)
		menu.add_cascade(label="关于",menu=about_menu)
		menu.add_cascade(label="作者微博：@AskeyNil,@一棵木鱼",menu=author_menu)
		self.root['menu'] = menu


		## 建立三个tab页
		tabControl = ttk.Notebook(self.root)
		tab1 = ttk.Frame(tabControl)
		tabControl.add(tab1, text='自动评论')
		tabControl.pack(expand=1, fill="both")
		tab2 = Frame(tabControl)
		tabControl.add(tab2, text='自动登录发帖')
		tab3 = Frame(tabControl)
		tabControl.add(tab3, text='判断链接')
		self.setup_talk_UI(tab1)
		self.setup_send_UI(tab2)
		self.setup_link_UI(tab3)

	def setup_talk_UI(self, view):
		## 主要两个底视图
		leftView = Frame(view, width=480, height=600)
		leftView.grid(row=0, column=1)
		rightView = Frame(view,width=170, height=600)
		rightView.grid(row=0, column=2)
		#固定容器大小
		leftView.grid_propagate(0)
		rightView.grid_propagate(0)
		# 建立左边的界面

		# 评论链接Label
		self.tab1_talk_link_text = StringVar()
		Label(leftView, textvariable=self.tab1_talk_link_text).grid(sticky=W)
		self.tab1_talk_link_text.set("评论链接：")
		# 评论链接的list
		self.tab1_link_list_value = StringVar()
		Listbox(leftView,listvariable=self.tab1_link_list_value,width=70,height=15).grid(row=1)

		# 话术文本的label和list
		Label(leftView,text="话术文本：").grid(row=2,sticky=W)
		self.tab1_talk_list_value = StringVar()
		self.tab1_talk_list_value.set(tuple(all_talks))
		listbox = Listbox(leftView,listvariable=self.tab1_talk_list_value, width=70,height=15).grid(row=3)


		topView = Frame(rightView)
		topView.grid(row=0,column=0)


		Label(topView,text="",height=1).grid(row=0,column=0)
		# 按钮
		btnSend = Button(topView, text='选择链接文本',width = 15,command=self.tab1_open_link)
		btnSend.grid(row=1,column=0,pady=5)


		btnCancel = Button(topView, text='选择评论话术', width = 15,command=self.tab1_open_talk)
		btnCancel.grid(row=2,column=0,pady=5)
		rightView.grid(row=0, column=2, rowspan=3,padx=2,pady=3)

		Button(topView, text='开始', width = 15, command=self.start_talk).grid(row=3,column=0,pady=5)
		Button(topView, text='停止', width = 15, command=self.stop_talk).grid(row=4,column=0,pady=5)
		Button(topView, text='暂停', width = 15, command=self.pasue_talk).grid(row=5,column=0,pady=5)


		bottomView = Frame(rightView)
		bottomView.grid(row=1,column=0)

		self.tab1_now_count_text = StringVar()
		self.tab1_sum_count_text = StringVar()
		self.tab1_style_text = StringVar()
		self.tab1_add_count_text = StringVar()
		self.tab1_sum_time_text = StringVar()
		self.tab1_now_time_text = StringVar()
		Label(bottomView,textvariable=self.tab1_style_text).grid(row=0,column=0,pady=10)
		Label(bottomView,textvariable=self.tab1_add_count_text).grid(row=2,column=0,pady=5)
		Label(bottomView,textvariable=self.tab1_sum_count_text).grid(row=3,column=0,pady=5)	## 总评论数
		Label(bottomView,textvariable=self.tab1_sum_time_text).grid(row=4,column=0,pady=5)	## 总评论花费时间
		Label(bottomView,textvariable=self.tab1_now_count_text).grid(row=5,column=0,pady=5)	## 当前评论数
		Label(bottomView,textvariable=self.tab1_now_time_text).grid(row=6,column=0,pady=5)	## 当前评论花费时间

		self.tab1_sum_count_text.set("总评论数：0条")
		self.tab1_now_count_text.set("当前评论数：0条")
		self.tab1_style_text.set("当前状态：停止")
		self.tab1_add_count_text.set("当前未导入文件")
		self.tab1_sum_time_text.set("总计用时：0秒")
		self.tab1_now_time_text.set("当前账号用时：0秒")
		imgInfo = PhotoImage(file = '1.gif')
		lblImage = Label(bottomView, image = imgInfo)
		lblImage.image = imgInfo
		lblImage.grid(row=8,column=0,sticky=S)


		## tab1的必备参数
		self.tab1_start = False
		self.tab1_pasue = False
		self.tab1_stop = True
		self.tab1_sum_count = 0		## 评论个数
		self.tab1_now_count = 0		## 当前账号评论个数
		self.tab1_timing = False 	## 是否计时
		self.tab1_sum_time = 0		## 评论总时间
		self.tab1_now_time = 0		## 当前账号评论时间
		self.tab1_urls = []
		self.tab1_talks = all_talks
		self.tab1_loop_time = 0		

	def tab1_open_link(self):
		if self.tab1_stop != True:
			tkinter.messagebox.showerror("警告","脚本已经在执行，请先\"停止\"脚本在运行导入操作")
			return
		if tkinter.messagebox.askyesno("温馨提示","是否要删除之前导入的链接"):
			self.tab1_link_list_value.set(())
			self.tab1_urls = []

		filename = tkinter.filedialog.askopenfilename(filetypes = [('TXT', 'txt')])
		if filename != '':
			urls_files = open(filename, 'r')
			self.tab1_talk_link_text.set(u"评论链接：" + filename)
			urls = urls_files.readlines()
			# 去重操作
			urls = list(set(urls))
			for url in urls:
				temp = url.strip()
				if temp == '':
					urls.remove(url)

			for index, url in enumerate(urls):
				urls[index] = url.strip()
			urls = list(set(urls))
			#print urls
			self.tab1_urls.extend(urls)
			self.tab1_add_count_text.set("当前有效链接数：" + str(len(self.tab1_urls)) + "条")
			self.tab1_link_list_value.set(tuple(self.tab1_urls))

	def tab1_open_talk(self):

		if self.tab1_stop != True:
			tkinter.messagebox.showerror("警告","脚本已经在执行，请先\"停止\"脚本在运行导入操作")
			return
		if tkinter.messagebox.askyesno("温馨提示","是否要删除之前导入的评论"):
			self.tab1_talk_list_value.set(())
		filename = tkinter.filedialog.askopenfilename(filetypes = [('TXT', 'txt')])
		if filename != '':
			talk_files = open(filename, 'r')
			talks = []
			for eachLine in talk_files:
				line = eachLine.strip() ## .decode('gbk', 'utf-8') # no decode in python3
				talks.append(line)

			for index, url in enumerate(talks):
				if url == u'' or url == u"\n" or url == u"" or url == u'\n':
					talks.remove(url)
					continue
			self.tab1_talks.extend(talks)
			self.tab1_talk_list_value.set(tuple(self.tab1_talks))

	def start_talk(self):
		if len(self.tab1_urls) == 0:
			tkinter.messagebox.showerror("温馨提示","请选择链接文本！！！！")
			self.tab1_start = False
			self.tab1_stop = True
			return

		if len(self.tab1_talks) == 0:
			tkinter.messagebox.showerror("温馨提示","请选择评论话术！！！！")
			self.tab1_start = False
			self.tab1_stop = True
			return


		if self.tab1_start == True:
			tkinter.messagebox.showerror("温馨提示","脚本已经在运行，请勿重复操作")
			return
		if tkinter.messagebox.askyesno("温馨提示","确定开始运行程序吗？"):
			self.tab1_style_text.set("当前状态：运行")
			self.tab1_start = True
			self.tab1_stop = False
			if self.tab1_pasue == True:
				self.tab1_pasue = False
			else:
				def loop():
					self.tab1_open_url()
				loopThread = threading.Thread(target=loop, name='tab1')
				loopThread.setDaemon(True)
				loopThread.start()


	def stop_talk(self):   #停止
		if self.tab1_start == False:
			tkinter.messagebox.showerror("温馨提示","程序未运行!!!")
			return
		if tkinter.messagebox.askyesno("温馨提示","确定要停止程序吗"):
			self._stop_talk()
	def _stop_talk(self):
		self.tab1_timing = False
		self.tab1_start = False
		self.tab1_stop = True
		self.tab1_style_text.set("当前状态：停止")

	def pasue_talk(self):  #暂停
		if self.tab1_stop == True:
			tkinter.messagebox.showerror("温馨提示","当前程序处于停止状态!!")
			return
		if self.tab1_start == False:
			tkinter.messagebox.showerror("温馨提示","程序未运行!!!")
			return
		if tkinter.messagebox.askyesno("温馨提示","确定要暂停程序吗？"):
			self.tab1_pasue = True
			self.tab1_start = False
			self.tab1_style_text.set("当前状态：暂停")

	def tab1_open_url(self):

		try:
			self.tab1_driver.get(home_url)  # 打开链接
		except:
			# self.tab1_driver = webdriver.Firefox()
			self.tab1_driver = webdriver.Chrome(executable_path = os.getcwd() + '/chromedriver')
			self.tab1_driver.get(home_url)  # 打开链接

		self.tab1_style_text.set("当前状态：等待登录")
		while is_login(self.tab1_driver) == False:
			if self.tab1_stop == True or self.tab1_pasue == True:
				self._stop_talk()
				return
		self.post_talks()

		# ## 开一个线程处理登录判断程序
		# def loop():
		# 	self.tab1_style_text.set("当前状态：等待登录")
		# 	while is_login(self.tab1_driver) == False:
		# 		if self.tab1_stop == True or self.tab1_pasue == True:
		# 			self._stop_talk()
		# 			return
		# 	self.post_talks()
		# loopThread = threading.Thread(target=loop, name='LoopThread')
		# loopThread.setDaemon(True)
		# loopThread.start()




	def post_talks(self):

		self.tab1_now_count = 0

		self.tab1_style_text.set("当前状态：运行")
		self.tab1_driver.refresh()
		# ele_id = "_btn_follow"
		# param = (By.ID,ele_id)
		# WebDriverWait(self.tab1_driver,10).until(EC.visibility_of_element_located(param))
		# print 123456
		## 判断是否关注
		btn_follow = self.tab1_driver.find_element_by_id("_btn_follow")
		follow_text = ""
		try:
			follow_text = btn_follow.get_attribute("style")
		except:
			follow_text = ""
		if follow_text != "display: none;":
			btn_follow.click()


		## 判断是否签到
		btn_dao = self.tab1_driver.find_element_by_id("_btn_signup")
		dao_text = ""
		try:
			dao_text = btn_follow.get_attribute("disabled")
		except:
			dao_text = ""
		if dao_text != "disabled":
			try:
				btn_dao.click()
			except Exception as e:
				pass



		self.tab1_timing = True

		for index, url in enumerate(self.tab1_urls):

			if url == "\n":
				continue
			if "http" not in url:
				loses_files = open(u'失效链接.txt', 'a+')
				self.tab1_urls.remove(url)
				loses_files.write(url)
				loses_files.write("\n")
				loses_files.close()
				continue

			## 判断是否是pc_url
			temp_url = pc_url(url)
			if pc_url(url) != url:
				url = temp_url
				self.tab1_urls[index] = temp_url


			if "id=1661556" not in url :
				self.queue.put("tab1_error,,"+ url)
				self._stop_talk()
				return


			self.tab1_driver.get(url)

			## 判断网页是否丢失
			try:
				text = self.tab1_driver.find_element_by_id("comment_txt")
			except:
				## 页面丢失的情况 写入错误
				loses_files = open(u'失效链接.txt', 'a+')
				self.tab1_urls.remove(url)
				loses_files.write(url)
				loses_files.write("\n")
				loses_files.close()
				continue

			meta = self.tab1_driver.find_element_by_class_name("article_meta").find_element_by_tag_name('a')
			flag = meta.get_attribute('data-flag')
			if flag == "1":
				meta.click()

			## 获取本页面的评论数
			try:
				max_count = int(self.tab1_driver.find_element_by_class_name("_comment_num").text)
			except:
				max_count = 0

			##正常运作
			text.click()
			talk = random.choice(self.tab1_talks)
			text.send_keys(talk)
			time.sleep(100)
			WebDriverWait(self.tab1_driver, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "btn_submit _valid_browser active")))
			self.tab1_driver.find_element_by_id("comment_submit").click()
			self.tab1_loop_time = 0
			## 判断时候提交完毕
			add_count = max_count
			while add_count >= max_count:
				if self.tab1_loop_time > 10:
					break
				try:
					max_count = int(self.tab1_driver.find_element_by_class_name("_comment_num").text)
				except:
					max_count = 0

			success_files = open(u'成功评论.txt', 'a+')
			success_files.write(url)
			success_files.write("\n")
			success_files.close()

			## 判断是否大于35
			if max_count > 32:
				max_files = open(u'评论数大于32.txt', 'a+')
				self.tab1_urls.remove(url)
				max_files.write(url)
				max_files.write("\n")
				max_files.close()
			else:
				effective_fies = open(u'有效链接.txt', 'a+')
				effective_fies.write(url)
				effective_fies.write("\n")
				effective_fies.close()
			self.tab1_sum_count = self.tab1_sum_count + 1
			self.tab1_now_count = self.tab1_now_count + 1
			## 反馈到label上
			self.tab1_sum_count_text.set("总评论数："+ str(self.tab1_sum_count) + "条")
			self.tab1_now_count_text.set("当前评论数："+ str(self.tab1_now_count) + "条")


			## 如果程序按下暂停键
			while self.tab1_pasue == True:
				pass

			# 判断时候按下停止
			if self.tab1_stop == True:
				self.tab1_driver.get(home_url)
				self.tab1_link_list_value.set(tuple(self.tab1_urls))
				return

		self.tab1_timing = False
		self.tab1_link_list_value.set(tuple(self.tab1_urls))

		#退出登录 回到主页面
		self.tab1_driver.delete_all_cookies()
		self.tab1_driver.get(home_url)

		## 发送消息
		self.queue.put("tab1_stop")

		self.tab1_style_text.set("当前状态：更换账号")
		while is_login(self.tab1_driver) == False:
			if self.tab1_stop == True or self.tab1_pasue == True:
				self._stop_talk()
				return
		self.post_talks()


	def setup_send_UI(self, view):
		leftView = Frame(view, width=480, height=600)
		leftView.grid(row=0, column=1)
		rightView = Frame(view,width=170, height=600)
		rightView.grid(row=0, column=2)
		#固定容器大小
		leftView.grid_propagate(0)
		rightView.grid_propagate(0)
		# 建立左边的界面

        ## change to login account info

		# # 评论链接Label
		# self.tab2_send_link_text = StringVar()
		# Label(leftView, textvariable=self.tab2_send_link_text).grid(sticky=W)
		# self.tab2_send_link_text.set("发帖链接：")
		# # 评论链接的list
		# self.tab2_send_list_value = StringVar()
		# Listbox(leftView,listvariable=self.tab2_send_list_value,width=70,height=15).grid(row=1)

        # 自动登录账户Label
		self.tab2_account_text = StringVar()
		Label(leftView, textvariable=self.tab2_account_text).grid(sticky=W)
		self.tab2_account_text.set("帐户信息：")
		# 自动登录账户的list
		self.tab2_accounts_list_value = StringVar()
		Listbox(leftView,listvariable=self.tab2_accounts_list_value,width=70,height=15).grid(row=1)

		# 话术文本的label和list
		Label(leftView,text="话术文本：").grid(row=2,sticky=W)
		self.tab2_talk_list_value = StringVar()
		self.tab2_talk_list_value.set(tuple(all_talks))
		listbox = Listbox(leftView,listvariable=self.tab2_talk_list_value, width=70,height=15).grid(row=3)


		topView = Frame(rightView)
		topView.grid(row=0,column=0)


		Label(topView,text="",height=1).grid(row=0,column=0)
		## 按钮
		btnSend = Button(topView, text='选择帐户文本',width = 15,command=self.tab2_open_account)
		btnSend.grid(row=1,column=0,pady=5)

		btnCancel = Button(topView, text='选择评论话术', width = 15,command=self.tab2_open_talk)
		btnCancel.grid(row=2,column=0,pady=5)
		rightView.grid(row=0, column=2, rowspan=3,padx=2,pady=3)

		Button(topView, text='开始', width = 15, command=self.start_send).grid(row=3,column=0,pady=5)
		Button(topView, text='停止', width = 15, command=self.stop_send).grid(row=4,column=0,pady=5)
		Button(topView, text='暂停', width = 15, command=self.pasue_send).grid(row=5,column=0,pady=5)
		self.tab2_send_count_text = StringVar()
		topBottomView = Frame(topView, width = 30,height = 1)
		topBottomView.grid(row=6,pady=5)
		Entry(topBottomView, width = 5,textvariable=self.tab2_send_count_text).grid(row=0,column=1)
		Label(topBottomView,text='发帖数量：').grid(row=0,column=0)
		self.tab2_send_count_text.set("5")
		# text.window_create(INSERT,window=b1)

		bottomView = Frame(rightView)
		bottomView.grid(row=1,column=0)

		self.tab2_sum_count_text = StringVar()
		self.tab2_success_count_text = StringVar()
		self.tab2_failed_count_text = StringVar()
		self.tab2_frozen_count_text = StringVar()
		self.tab2_style_text = StringVar()

		self.tab2_sum_time_text = StringVar()
		self.tab2_now_time_text = StringVar()
		Label(bottomView,textvariable=self.tab2_style_text).grid(row=0,column=0,sticky=N,pady=30)
		Label(bottomView,textvariable=self.tab2_sum_count_text).grid(row=3,column=0,pady=5)	## 总评论数
		Label(bottomView,textvariable=self.tab2_sum_time_text).grid(row=4,column=0,pady=5)	## 总评论花费时间
		Label(bottomView,textvariable=self.tab2_success_count_text).grid(row=5,column=0,pady=5)	## 当前评论数
		Label(bottomView,textvariable=self.tab2_failed_count_text).grid(row=6,column=0,pady=5)	## 当前评论花费时间
		Label(bottomView,textvariable=self.tab2_frozen_count_text).grid(row=7,column=0,pady=5)	## 当前评论花费时间

		self.tab2_sum_count_text.set("帐户总数：0")
		self.tab2_success_count_text.set("成功登录帐户数：0")
		self.tab2_style_text.set("当前状态：停止")
		self.tab2_sum_time_text.set("总计用时：0秒")
		self.tab2_failed_count_text.set("密码错误帐户数：0")
		self.tab2_frozen_count_text.set("冻结帐户数：0")

		imgInfo = PhotoImage(file = '2.gif')
		lblImage = Label(bottomView, image = imgInfo)
		lblImage.image = imgInfo
		lblImage.grid(row=8,column=0,sticky=S)

		## tab1的必备参数
		self.tab2_start = False
		self.tab2_pasue = False
		self.tab2_stop = True
		self.tab2_sum_count_account = 0		## 当前帐号总数
		self.tab2_now_count_account = 0		## 当前成功账号个数
		self.tab2_count_account_frozen = 0	## 冻结帐户个数
		self.tab2_count_account_failed = 0	## 密码错误帐户个数
		self.tab2_sum_count = 0		## 评论个数
		self.tab2_now_count = 0		## 当前账号评论个数
		self.tab2_timing = False 	## 是否计时
		self.tab2_sum_time = 0		## 评论总时间
		self.tab2_now_time = 0		## 当前账号评论时间
		self.tab2_accounts = []
		self.tab2_talks = all_talks

	def start_send(self):
		if len(self.tab2_talks) == 0:
			tkinter.messagebox.showerror("温馨提示","请选择评论话术！！！！")
			self.tab2_start = False
			self.tab2_stop = True
			return
		if self.tab2_start == True:
			tkinter.messagebox.showerror("温馨提示","脚本已经在运行，请勿重复操作")
			return
		count = 0
		try:
			count = int(self.tab2_send_count_text.get())
		except:
			count = 0
		if count <= 0:
			tkinter.messagebox.showerror("温馨提示","发帖数量应是大于等于1的数字")
			return

		if tkinter.messagebox.askyesno("温馨提示","确定开始运行程序吗？"):
			self.tab2_style_text.set("当前状态：运行")
			self.tab2_start = True
			self.tab2_stop = False
			if self.tab2_pasue == True:
				self.tab2_pasue = False
			else:
				def loop():
					self.tab2_open_url()
				loopThread = threading.Thread(target=loop, name='tab2')
				loopThread.setDaemon(True)
				loopThread.start()

	def stop_send(self):
		if self.tab2_start == False:
			tkinter.messagebox.showerror("温馨提示","程序未运行!!!")
			return
		if tkinter.messagebox.askyesno("温馨提示","确定要停止程序吗"):
			self._stop_send()

	def _stop_send(self):
		self.tab2_timing = False
		self.tab2_start = False
		self.tab2_stop = True
		self.tab2_style_text.set("当前状态：停止")

	def pasue_send(self):
		if self.tab2_stop == True:
			tkinter.messagebox.showerror("温馨提示","当前程序处于停止状态!!")
			return
		if self.tab2_start == False:
			tkinter.messagebox.showerror("温馨提示","程序未运行!!!")
			return
		if tkinter.messagebox.askyesno("温馨提示","确定要暂停程序吗？"):
			self.tab2_pasue = True
			self.tab2_start = False
			self.tab2_style_text.set("当前状态：暂停")

	def tab2_open_url(self):

		try:
			self.tab2_driver.get(home_url)  # 打开链接
		except:
			# self.tab2_driver = webdriver.Firefox()
			self.tab2_driver = webdriver.Chrome(executable_path = os.getcwd() + '/chromedriver')
			self.tab2_driver.get(home_url)  # 打开链接

		self.tab2_style_text.set("当前状态：等待登录")
		# while is_login(self.tab2_driver) == False:
		# 	if self.tab2_stop == True or self.tab2_pasue == True:
		# 		self._stop_send()
		# 		return

        # for


		self.tab2_login()
		#self.send_talks()


	def tab2_login(self):
		self.tab2_driver.refresh()
		self.tab2_timing = True
		self.tab2_success_count_account = 0
		self.tab2_failed_count_account = 0
		self.tab2_frozen_count_account = 0
		autoLogin = dokiLogin(self)
		# get accounts
		# accounts = autoLogin.get_account_info("accounts.txt")
		# accounts_failed = {}
		for account in self.tab2_accounts:
			user, pw = account.strip().split("----")
			autoLogin.to_continue = False
			# try:
			if autoLogin.login(user, pw):
				pass
			else:
				fails = 0
				while fails < 3 and not autoLogin.frame_relogin(user, pw):
					#print(fails)
					#print("登录再次失败")
					fails += 1
				if fails == 3:
					autoLogin.write_failed_account(user, pw)
					self.tab2_failed_count_account += 1
					#print("该帐号用户名密码不可用，即将换号操作\n")
			#print(autoLogin.to_continue)
			if autoLogin.to_continue:
				autoLogin.write_success_account(user, pw)
				self.tab2_success_count_account += 1
				self.send_talks()
			self.tab2_frozen_count_account = autoLogin.frozen_count
			autoLogin.driver.delete_all_cookies()
			self.tab2_driver.get(home_url)
			#print("\n")
			# except Exception:
			# 	autoLogin.write_frozen_account(user, pw)
			# 	print("该帐号被锁，登录失败\n")
			# 	autoLogin.driver.delete_all_cookies()
			# 	self.tab2_driver.get(home_url)

			self.tab2_success_count_text.set("成功登录帐户数："+ str(self.tab2_success_count_account))
			self.tab2_failed_count_text.set("密码错误帐户数："+ str(self.tab2_failed_count_account))
			self.tab2_frozen_count_text.set("冻结帐户数："+ str(self.tab2_frozen_count_account))


			## 如果程序按下暂停键
			while self.tab2_pasue == True:
				pass

			# 判断时候按下停止
			if self.tab2_stop == True:
				self.tab2_driver.get(home_url)
				return
			

		self.tab2_timing = False
		self.tab2_driver.delete_all_cookies()
		self.tab2_driver.get(home_url)
		## 切换账号
		self.queue.put("tab2_stop")
		self.tab2_style_text.set("当前状态：等待下组账号")
		self._stop_send()
		

    # def account_login(self):


	def send_talks(self):

		# self.tab2_driver.refresh()
        #
		# self.tab2_timing = True
		## 判断是否关注
		btn_follow = self.tab2_driver.find_element_by_id("_btn_follow")
		follow_text = ""
		try:
			follow_text = btn_follow.get_attribute("style")
		except:
			follow_text = ""
		if follow_text != "display: none;":
			btn_follow.click()


		## 判断是否签到
		btn_dao = self.tab2_driver.find_element_by_id("_btn_signup")
		dao_text = ""
		try:
			dao_text = btn_follow.get_attribute("disabled")
		except:
			dao_text = ""
		if dao_text != "disabled":
			try:
				btn_dao.click()
			except Exception as e:
				pass

		count = int(self.tab2_send_count_text.get())
		for x in range(1,count+1): ## xrange(1,count+1):
			# 查找发帖
			self.tab2_driver.get(post_url)
			title = self.tab2_driver.find_element_by_id("note_title")
			title.click()
			title_text = random.choice(titles)
			title.send_keys(title_text)
			time.sleep(0.5)
			context_text = random.choice(self.tab2_talks)
			context = self.tab2_driver.find_element_by_id("note_content")
			context.click()
			context.send_keys(context_text)
			time.sleep(0.5)
			btn = self.tab2_driver.find_element_by_id("note_pub")
			try:
				btn.click()
			except Exception as e:
				continue
			while "https://v.qq.com/doki/doki_note/detail" not in self.tab2_driver.current_url:
				pass
			## self.tab2_urls.append(self.tab2_driver.current_url)
			link_files = open(u'链接.txt', 'a+')
			link_files.write(self.tab2_driver.current_url)
			link_files.write("\n")
			link_files.close()
			self.tab2_sum_count = self.tab2_sum_count + 1
			self.tab2_now_count = self.tab2_now_count + 1
			# self.tab2_send_list_value.set(tuple(self.tab2_urls)) ## no need to send list to ui anymore

			## 如果程序按下暂停键
			while self.tab2_pasue == True:
				pass

			# 判断时候按下停止
			if self.tab2_stop == True:
				self.tab2_driver.get(home_url)
				return

		self.tab2_now_count_account += 1
		#print("该帐号发帖完成！")

    ## function for opening account file in tab2
	def tab2_open_account(self):
		if self.tab2_stop != True:
			tkinter.messagebox.showerror("警告","脚本已经在执行，请先\"停止\"脚本在运行导入操作")
			return
		if tkinter.messagebox.askyesno("温馨提示","是否要删除之前导入的帐户"):
			self.tab2_accounts_list_value.set(())
		filename = tkinter.filedialog.askopenfilename(filetypes = [('TXT', 'txt')])
		if filename != '':
			account_files = open(filename, 'r')
			accounts = []
			for eachLine in account_files:
				line = eachLine.strip() ## .decode('gbk', 'utf-8') # no decode in python3
				accounts.append(line)

			for index, account in enumerate(accounts):
				if account == '' or account == "\n" or account == "" or account == '\n':
                # if account == u'' or account == u"\n" or account == u"" or account == u'\n': ## change for python3
					accounts.remove(account)
					continue
			accounts = list(set(accounts))
			self.tab2_accounts.extend(accounts)
			self.tab2_sum_count_account = len(self.tab2_accounts)
			self.tab2_accounts_list_value.set(tuple(self.tab2_accounts))
			self.tab2_sum_count_text.set("帐户总数："+ str(self.tab2_sum_count_account))
		pass


	def tab2_open_talk(self):
		if self.tab2_stop != True:
			tkinter.messagebox.showerror("警告","脚本已经在执行，请先\"停止\"脚本在运行导入操作")
			return
		if tkinter.messagebox.askyesno("温馨提示","是否要删除之前导入的评论"):
			self.tab2_talk_list_value.set(())
		filename = tkinter.filedialog.askopenfilename(filetypes = [('TXT', 'txt')])
		if filename != '':
			talk_files = open(filename, 'r')
			talks = []
			for eachLine in talk_files:
				line = eachLine.strip() ## .decode('gbk', 'utf-8') # no decode in python3
				talks.append(line)

			for index, url in enumerate(talks):
				if url == u'' or url == u"\n" or url == u"" or url == u'\n':
					talks.remove(url)
					continue
			self.tab2_talks.extend(talks)
			self.tab2_talk_list_value.set(tuple(self.tab2_talks))
		pass

	def setup_link_UI(self, view):

		leftView = Frame(view, width=480, height=600)
		leftView.grid(row=0, column=1)
		rightView = Frame(view,width=170, height=600)
		rightView.grid(row=0, column=2)
		#固定容器大小
		leftView.grid_propagate(0)
		rightView.grid_propagate(0)



		# 评论链接Label
		self.tab3_send_link_text = StringVar()
		Label(leftView, textvariable=self.tab3_send_link_text).grid(sticky=W)
		self.tab3_send_link_text.set("链接：")
		# 评论链接的list
		self.tab3_send_list_value = StringVar()
		Listbox(leftView,listvariable=self.tab3_send_list_value,width=70,height=30).grid(row=1)

		padx = 0

		Label(rightView,text="").grid(row=0,column=0,pady=5,sticky=W)
		self.tab3_keys_text = StringVar()

		btnSend = Button(rightView, text='选择链接文本',width = 15,command=self.tab3_open_link)
		btnSend.grid(row=1,column=0,pady=5)
		Label(rightView,text='授权码：').grid(row=2,column=0,sticky=W, pady=5)
		Entry(rightView, width = 15,textvariable=self.tab3_keys_text).grid(row=3,column=0,pady=5)
		talk_view = Frame(rightView, width = 10,height = 1)
		talk_view.grid(row=4,column=0)
		self.tab3_talk_count = StringVar()
		Label(talk_view,text='筛选评论数小于：').grid(row=0,column=0,sticky=W, pady=5)
		Entry(talk_view, width = 3,textvariable=self.tab3_talk_count).grid(row=0,column=1, pady=5)
		self.tab3_talk_count.set(32)
		self.tab3_all_text = StringVar()
		self.tab3_now_text = StringVar()
		self.tab3_visable_text = StringVar()
		Button(rightView, text='开始', width = 15, command=self.start_change).grid(row=5,column=0,padx=padx,pady=5)
		Label(rightView,textvariable=self.tab3_all_text).grid(row=6,column=0,pady=5,padx=padx)
		Label(rightView,textvariable=self.tab3_now_text).grid(row=7,column=0,pady=5,padx=padx)
		Label(rightView,textvariable=self.tab3_visable_text).grid(row=8,column=0,pady=5,padx=padx)
		self.tab3_all_text.set("总数：0条")
		self.tab3_now_text.set("已完成：0条")
		self.tab3_visable_text.set("有效链接:0条")

		self.tab3_urls = []
		self.tab3_start = False


	def tab3_open_link(self):
		if self.tab3_start == True:
			tkinter.messagebox.showerror("警告","脚本已经在执行，请等待执行结束")
			return
		if tkinter.messagebox.askyesno("温馨提示","是否要删除之前导入的链接"):
			self.tab3_send_list_value.set(())
			self.tab3_urls = []

		filename = tkinter.filedialog.askopenfilename(filetypes = [('TXT', 'txt')])
		if filename != '':
			urls_files = open(filename, 'r')
			self.tab3_send_link_text.set(u"链接：" + filename)
			urls = urls_files.readlines()
			# 去重操作
			urls = list(set(urls))
			for url in urls:
				temp = url.strip()
				if temp == '':
					urls.remove(url)

			for index, url in enumerate(urls):
				urls[index] = url.strip()
			urls = list(set(urls))
			#print urls
			self.tab3_urls.extend(urls)
			self.tab3_all_text.set("总数：{}条".format(len(self.tab3_urls)))
			self.tab3_send_list_value.set(tuple(self.tab3_urls))


	def start_change(self):
		# 判断授权码
		if self.tab3_keys_text.get() != "cyh19971017":
			tkinter.messagebox.showerror("温馨提示","请输入正确的授权码")
			self.tab3_start = False
			return
		if len(self.tab3_urls) == 0:
			tkinter.messagebox.showerror("温馨提示","请选择转化链接！！！！")
			self.tab3_start = False
			return
		if self.tab3_start == True:
			tkinter.messagebox.showerror("温馨提示","脚本已经在运行，请勿重复操作")
			return
		count = 0
		try:
			count = int(self.tab3_talk_count.get())
		except:
			count = 0
		if count <= 0:
			tkinter.messagebox.showerror("温馨提示","筛选评论数应是大于等于1的数字")
			return
		self.tab3_count = count
		if tkinter.messagebox.askyesno("温馨提示","确定开始运行程序吗？"):

			self.tab3_start = True
			def loop():
				self.tab3_open_url()
			loopThread = threading.Thread(target=loop, name='tab3')
			loopThread.setDaemon(True)
			loopThread.start()
	def tab3_open_url(self):
		self.tab3_now_text.set("已完成：0条")
		self.tab3_visable_text.set("有效链接:0条")
		now_count = 0
		for index, url in enumerate(self.tab3_urls):

			if "http" not in url:
				continue
			text = pc_url(url)
			url = requests.get(text).text
			try:
				url = url.split("_comment_num\">")[1]
				url = url.split("</span>")[0]
			except:
				url = 9999999
			if int(url) < self.tab3_count:
				now_count = now_count + 1
				self.tab3_visable_text.set("有效链接:{}条".format(now_count))
				oktalk = open(u'评论小于{}条.txt'.format(self.tab3_count), 'a')
				oktalk.write(text)
				if "\n" not in text:
					oktalk.write("\n")
				oktalk.close()
			else:
				oktalk = open(u'有问题或评论超过{}条.txt'.format(self.tab3_count), 'a')
				oktalk.write(text)
				if "\n" not in text:
					oktalk.write("\n")
				oktalk.close()
			self.tab3_now_text.set("已完成：{}条".format(index+1))

		self.queue.put("tab3_stop")
		self.tab3_start = False



if __name__ == "__main__":
	# try:
	ApplicationUI()
	# except Exception as e:
		# print e


#
