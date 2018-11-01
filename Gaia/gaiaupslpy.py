
import os
import urllib
import requests
import tempfile


def gaia_upload_f(url, filePath):

    """
    上传单个文件到服务器
    @url : gaia服务器地址
    @filePath: 本地文件路径
    """
    filename = os.path.basename(filePath)
    headers = {"gress_checker" : "__gaiafintech__"};

    files = {filename: (filename, open(filePath, 'rb'))}
    rsp = requests.post(url, headers = headers, files = files)

    return rsp.text

def gaia_upload_u(url, srcUrl):

    """
    将srcUrl 的文件 转储到 gaia 资源服务
    @url : 服务器地址
    @filePath: 网络上的文件url
    """
    filename = os.path.basename(srcUrl)
    tpfath = urllib.request.urlretrieve(srcUrl)[0];
    headers = {"gress_checker" : "__gaiafintech__"};
    files = {filename: (filename, open(tpfath, 'rb'))}
    rsp = requests.post(url, headers = headers, files = files)

    return rsp.text

###########################################################################
if __name__ == "__main__" :
    
    ##测试上传本地文件到服务器
    url = "http://gress.gaiafintech.com/upload"
    filePath = "C:\\Users\\gaia-develop\\Desktop\\test.txt"
    text = gaia_upload_f(url, filePath)

    print(text)

    ## 测试转发某图片url 的图片到服务器
    srcUrl = "https://www.baidu.com/favicon.ico"
    text = gaia_upload_u(url, srcUrl)
    print(text)
###########################################################################