#coding=utf8
import urllib
import urllib2
import json
import time
from bs4 import BeautifulSoup
import MySQLdb

if __name__=='__main__':
	print 'main'
	#login()
	#execute()
	#renew()
	url = 'http://codecraft.devcloud.huaweicloud.com/home/living'
	url2 = 'http://codecraft.devcloud.huaweicloud.com//Home/TeamScoreDisplays'
	postdata={}
	postdata['stageKey']='报名/初赛'
	postdata['subKey']='6'
	postdata['stageType']='1'
	params = urllib.urlencode(postdata)
	request=urllib2.Request(url2,params)
	respose = urllib2.urlopen(request)
	html = respose.read()

	db = MySQLdb.connect("localhost", "username", "password", "database", charset="utf8")
	cursor = db.cursor()

	soup = BeautifulSoup(html, "lxml")
	trs = soup.find_all('tr')
	for tr in trs:
		tds = tr.find_all('td')
		for i in range(len(tds)):
			if i == 0:
				rank = tds[i].string
			if i == 1:
				teamName = tds[i].string
			if i == 2:
				captainName = tds[i].string
			if i == 3:
				schoolName = tds[i].string
			if i == 4:
				slogan = tds[i].string
			if i == 5:
				score = tds[i].string
		t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		#print '%d, %s, %s, %s, %s, %f'%(int(rank), teamName, captainName, schoolName, slogan, float(score))
		try:
			sql = "select * from score where teamName = '%s'"%teamName
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				id_ = row[0]
				teamName_ = row[1]
				captainName_ = row[2]
				schoolName_ = row[3]
				slogan_ = row[4]
				score_ = row[5]
				time_ = row[6]
			if float(score_) < float(score):
				print "need to update data for %s"%teamName
				sql = "update score set score=%f, time='%s' where teamName = '%s'"%(float(score),t,teamName)
				try:
					cursor.execute(sql)
					db.commit()
					print "update succeeded!"
				except:
					print "update data failed"
					db.rollback()
		except:
			print "No record for %s"%teamName
			sql = "insert into score(teamName,captainName,schoolName,slogan,score,time) values('%s','%s','%s','%s','%f','%s')"%(teamName, captainName, schoolName, slogan, float(score), t)
			#print sql
			try:
				cursor.execute(sql)
				db.commit()
				print "insert succeeded!"
			except:
				print "insert data failed."
				db.rollback()
	
	html = u""
	hhh = u"我的天"
	try:
		sql = 'select * from score'
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			id_ = row[0]
			teamName_ = row[1]
			captainName_ = row[2]
			schoolName_ = row[3]
			slogan_ = row[4]
			score_ = row[5]
			time_ = row[6]
			html = html+u"<tr class='tr-even'>\r\n<td class='first-td'>%d</td>\r\n<td title='%s'>%s</td>\r\n<td title='%s'>%s</td>\r\n<td title='%s'>%s</td>\r\n<td style='text-align:center' title='%s'>%s</td>\r\n<td class='score'>%f</td>\r\n</tr>\r\n"%(id_, teamName_, teamName_, captainName_, captainName_, schoolName_, schoolName_, slogan_, slogan_, score_)
	except:
		print "emmm..."
	print html
	html = u"<html>\r\n<head>\r\n<meta charset='utf8'>\r\n<title>codecraft 高分记录</title>\r\n</head><body><table class='fin-table'><thead><tr><th class='fin-table-first'>序号</th><th>团队名称</th><th>队长昵称</th><th>院校名称</th><th style='width:20%;text-align:center'>团队口号</th><th>成绩</th></tr></thead><tbody id='listData'>"+html
	html = html + u"</tbody></table></body></html>"
	db.close()
	f = open('codecraft.html','w')
	f.write(html.encode('utf8'))
	f.close()
