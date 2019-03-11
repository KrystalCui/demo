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

#新浪财经
class SinaFinanceNewsItem(Item):
    time = Field()
    title = Field()
    url = Field()
    page = Field()

#东方财富
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

#腾讯财经
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

class WorldFinanceItem(Item):
    datasource = Field()
    title = Field()
    url = Field()
    imagescr = Field()
    simdigest = Field()
    abouttime = Field()

class DomesticCommodityExchangeItem(Item):
    datasource = Field()
    #交易品种
    tradingvariety = Field()
    #交易单位
    tradingunit = Field()
    #报价单位
    quotationunit = Field()
    #最小变动价位
    minimumpricechange = Field()
    #涨跌停板幅度
    pricelimits = Field()
    #合约月份
    contractmonth = Field()
    #交易时间
    tradingtime = Field()
    #最后交易日
    lastNoticeDay = Field()
    #最后交割日
    finaldeliverydate = Field()
    #交割等级
    deliveryGrade = Field()
    #交割地点
    deliverypoints = Field()
    #最低交易保证金
    minimumtransactionmargin = Field()
    #交割方式
    deliverymethods = Field()
    #交易代码
    transactioncode = Field()
    #上市交易所
    listingexchange = Field()
    #容重
    bulkdensity = Field()
    #总量
    total = Field()
    #项目
    project = Field()
    #可交割国债
    deliverablenationaldebt = Field()
    #报价方式
    quotationmethod = Field()
    #交割日期
    deliverydate = Field()
    #最后交易日交易时间
    lasttradingdaytradingtime = Field()

#新浪,东财等资讯合集
class InformationAggregationItem(Item):
    # 摘要
    abstract = Field()
    # 内容
    content = Field()
    # 获取来源(如新浪,东财等)
    datasource = Field()
    # id
    _id = Field()
    # 图片URL
    imgURL = Field()
    # 作者
    newsauth = Field()
    # 时间
    newstime = Field()
    # 页面中显示来源
    source = Field()
    # 状态
    state = Field()
    # 子标题
    subtitle = Field()
    # 标题
    title = Field()












