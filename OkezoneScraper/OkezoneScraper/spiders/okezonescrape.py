# -*- coding: utf-8 -*-
import scrapy
from OkezoneScraper.items import Berita
import mysql.connector

class OkezonescrapeSpider(scrapy.Spider):
    name = 'okezonescrape'
    pages = range(0, 25000, 16)
    katakuncis = ('pembunuhan','penganiayaan','pencabulan','perbudakan','perampasan','pencurian','narkotika','penipuan','permusuhan')
    start_urls = []

    for katakunci in katakuncis:
        for page in pages:
            link = 'https://search.okezone.com/searchsphinx/loaddata/article/'+katakunci+'/'+str(page)
            start_urls.append(link)

    def parse(self, response):
        articles = response.css('div.title a::attr(href)').getall()
        for article in articles:
            yield scrapy.Request(article, callback=self.parse_article)
    
    def parse_article(self, response):
        #konek db
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "okezone"
            )
        mycursor = mydb.cursor()
        sumber = 'okezone'
        keyword = 'permusuhan'
        url = response.request.url
        tanggal = response.css('div.reporter div.namerep b::text').get()
        judul = response.css('div.title h1::text').get()
        tpt = response.css('div#contentx.read p strong::text').get()
        kontens = response.css('div#contentx.read p::text').getall()
        full = []
        full.append(tpt)
        for kontenn in kontens:
            full.append(kontenn)
        konten = ''.join(full)
        print('-',judul)
        #Masukin ke DB
        sql = "INSERT okezone VALUES (%s, %s, %s, %s, %s, %s)"
        baris = (
            sumber,
            keyword, 
            url, 
            tanggal,
            judul,
            konten)

        mycursor.execute(sql, baris)
        mydb.commit()
