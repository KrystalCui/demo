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

class CourseItem(Item):
    _id = Field()
    title = Field()
    number = Field()
    area = Field()
    huxing = Field()
    tel = Field()

class BossDirectEmploymentItem(Item):
    position_name = Field()
    salary1 = Field()
    salary2 = Field()
    address = Field()
    experience = Field()
    education = Field()
    line_business = Field()
    financing_stage = Field()
    employees = Field()
    issue_date = Field()
    job_description = Field()
    company_description = Field()

class SevenTwentyFourNewsItem(Item):
    _id = Field()
    title = Field()
    simtitle = Field()
    showtime = Field()
    ordertime = Field()
    digest = Field()
    simdigest = Field()
    url = Field()#即将跳转的网页
    commentnum = Field()

class SinaFinanceNewsItem(Item):
    time = Field()
    title = Field()
    url = Field()
    page = Field()

class NewsItem(Item):
    datasource = Field()
    imageurl = Field()  #点击图片后跳转的链接
    imagescr = Field()
    titleurl = Field()
    titletext = Field()
    contenttitle = Field()
    contenttext = Field()
    time = Field()
    localtime = Field()

class StockNewsItem(Item):
    datasource = Field()
    arttitle = Field()
    arturl = Field()
    artcreateTime = Field()
    artcontent = Field()
    localtime = Field()
    stockname = Field()

class QQFinanceItem(Item):
    _id = Field()
    imgscr = Field()
    url = Field()
    abouttime = Field()
    titletext = Field()

class FuturesExchangeItem(Item):
    productId = Field()
    productName = Field()
    productCode = Field()
    uri = Field()
    exchangeCode = Field()
    datasource = Field()

class ContractSpecificationsItem(Item):
    datasource = Field()
    productName = Field()
    ContractUnit = Field()
    PriceQuotation = Field()
    TradingHours = Field()
    MinimumPriceFluctuation = Field()
    ProductCode = Field()
    ListedContracts = Field()
    SettlementMethod = Field()
    TerminationOfTrading = Field()
    TradeAtMarkerOrTradeAtSettlementRules = Field()
    SettlementProcedures = Field()
    PositionLimits = Field()
    ExchangeRulebook = Field()
    BlockMinimum = Field()
    PriceLimitOrCircuit = Field()
    VendorCodes = Field()

