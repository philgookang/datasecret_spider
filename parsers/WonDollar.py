import requests
from bs4 import BeautifulSoup

from library.Parser import Parser


class WonDollar(Parser):


	def __init__(self, **kwargs):
		super(WonDollar, self).__init__(**kwargs)


	def parse(self):

		# get html page
		url = "https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page=1"
		html = requests.get(url).content

		# create parse element
		bs = BeautifulSoup(html, "html.parser")
		

		#BEGIN PARSE

		# get table row list
		trs = bs.find("table", class_="tbl_exchange today").find("tbody").find_all("tr")

		# loop through and update/add database
		for tr in trs:
			tds = tr.find_all("td")
			params = {
				"type" 					: "won",
				"date_price"			: tds[0].text.replace(".", "-"),
				"price" 				: tds[1].text.replace(",", ""),
				"price_change" 			: tds[2].text.replace(",", ""),
				"cash_buy_rate" 		: tds[3].text.replace(",", ""),
				"cash_sell_rate"		: tds[4].text.replace(",", ""),
				"transfer_buy_rate" 	: tds[5].text.replace(",", ""),
				"transfer_sell_rate" 	: tds[6].text.replace(",", ""),
				"tc_buy_rate" 			: tds[7].text.replace(",", "").strip(),
				"tc_foreign_sell" 		: tds[8].text.replace(",", "").strip(),
			}
		
