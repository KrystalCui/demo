# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class ParameterItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = Field()
    title = Field()
    source = Field()
    url = Field()
    content = Field()
    datetime = Field()
    parameter1 = Field()
    parameter2 = Field()

class InvestmentAdviserItem (Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = Field ()
    title = Field ()
    source = Field ()
    url = Field ()
    content = Field ()
    datetime = Field ()
    parameter1 = Field ()
    parameter2 = Field ()

class F10Item(Item):
    _id = Field ()
    underlyingIssueName = Field()
    priceTick = Field()
    exchangeDate = Field()
    underlyingIssueCode = Field()
    exchangeUnit = Field()
    upDownLimit = Field()
    deliveryGrade = Field()
    tradeMarket = Field()
    tickUnit = Field()
    deliveryDate = Field()
    deliveryAddress = Field()
    additionalInfo = Field()
