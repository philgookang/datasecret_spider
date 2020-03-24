import requests
from bs4 import BeautifulSoup
from datetime import datetime

from library.Parser import Parser
from library.Postman import Postman
from library.Log import LOG

class WonDollar(Parser):


	def __init__(self, **kwargs):
		super(WonDollar, self).__init__(**kwargs)
		self.cnt = 1


	def parse(self):

		# get html page
		#url = "https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page=1"
		url = "https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page=" + str(self.cnt)
		html = requests.get(url).content

		# create parse element
		bs = BeautifulSoup(html, "html.parser")

		# create postman class
		postman = Postman.init()
		

		#BEGIN PARSE

		# get table row list
		trs = bs.find("table", class_="tbl_exchange today").find("tbody").find_all("tr")

		# loop through and update/add database
		for tr in trs:
			tds = tr.find_all("td")

			# check for change is minus
			minus = "-" if tds[2].find("img").attrs["alt"] == "하락" else ""

			params = {
				"date_price"			: tds[0].text.replace(".", "-"),
				"price" 				: tds[1].text.replace(",", ""),
				"price_change" 			: minus + tds[2].text.replace(",", "").strip(),
				"cash_buy_rate" 		: tds[3].text.replace(",", ""),
				"cash_sell_rate"		: tds[4].text.replace(",", ""),
				"transfer_buy_rate" 	: tds[5].text.replace(",", ""),
				"transfer_sell_rate" 	: tds[6].text.replace(",", ""),
				"tc_buy_rate" 			: tds[7].text.replace(",", "").strip(),
				"tc_foreign_sell" 		: tds[8].text.replace(",", "").strip(),
			}
			
			# get item from database with current date
			check = postman.getObject("""
				SELECT idx FROM 
					`currency_rate` 
				WHERE 
						`type`=%s
					AND
						`date_price`=%s 
					AND 
						`status`=%s
			""", [ "DOLWON",  params["date_price"], "1" ])

			# check if there was any results
			if check and "idx" in check:
				LOG(self.name, params["date_price"], "already exists, skipping to next row")
				# result found, skip to next one!
				continue
			
			# if no results found, insert
			idx = postman.create("""
				INSERT INTO `currency_rate` (
					`type`, 
					`date_price`, 
					`price`,
					`price_change`,
					`cash_buy_rate`,
					`cash_sell_rate`,
					`transfer_buy_rate`,
					`transfer_sell_rate`,
					`tc_buy_rate`,
					`tc_foreign_sell`,
					`created_date_time`,
					`status`
				) VALUES (
					%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
				)
			""", [
				"DOLWON",
				params["date_price"], params["price"], params["price_change"], params["cash_buy_rate"],
				params["cash_sell_rate"], params["transfer_buy_rate"], params["transfer_sell_rate"],
				params["tc_buy_rate"], params["tc_foreign_sell"],
				str(datetime.now().strftime("%Y-%m-%d %H:%I:%S")), '1'
			])

			LOG(self.name, "created row with idx:", idx)
			LOG(self.name, params)


		self.cnt = self.cnt + 1
