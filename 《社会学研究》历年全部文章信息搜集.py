import requests
import bs4
import re
import numpy
import pytablewriter
from bs4 import BeautifulSoup

def gethtml(url):#获取网页内容
        try:
           r=requests.get(url)
           r.raise_for_status()
           r.encoding=r.apparent_encoding
           return r.text
        except:
           return ""  

def get_id(articul_id,html):#获取文章id
    try:
        soup=BeautifulSoup(html,"html.parser")
        idlinks=soup("a") 
        for ids in idlinks:
            if str(ids.get("href"))[:24]=="http://oa.shxyj.org/Stat":
                href=str(ids.get("href"))
                articul_id.append(re.findall(r"(?<==)[1-9]\d{0,4}|100000(?=&)",href))#正则表达式
        return(articul_id)
    except:
        return "获取文章id失败"
    
def get_info(articul_infos,articul_id,count):#获取文章信息
    try:
        
        for ids in articul_id:
            
            count+=1
            
            url="http://www.shxyj.org/Magazine/show/?id="+ids[0]#获取每一篇文章的地址
            html=gethtml(url)
            soup=BeautifulSoup(html,"html.parser")
            name=soup.title.get_text()#获取文章名
            link=soup.find_all("a")
            
            url=[]
            
            for i in link:
                if str(i.get("href"))[:24]=="http://oa.shxyj.org/Stat":
                    url.append(i.get("href"))#获取文章链接：一个在线，一个下载
                   
            authorinfo=soup.find_all("td")#作者信息

            info_lists=[]
            
            for info in authorinfo:
                info_lists.append(info.get_text())
            

            for i in range(11):
                info_lists.pop(len(info_lists)-1)#删除末尾无关信息

            info_lists.insert(0,name)#将文章名添加进列表

            articul_info=[count]+info_lists+url
            articul_infos.append(articul_info)
        
        return(articul_infos)
    except:
        return "获取文章信息失败"

    
def into_file(articul_infos):#将爬到的文章信息写入excel
    try:
        writer = pytablewriter.ExcelXlsxTableWriter()
        writer.open("《社会学研究》历年文章全集.xlsx")
        writer.make_worksheet("example")
        writer.header_list = ["序号", "篇名", "类目1", "英文标题", "类目2", "中文摘要","类目3","英文摘要","类目4","作者","类目5","作者单位","类目6","期刊","类目7","发表时间及页码","下载地址"]
        writer.value_matrix = articul_infos
        writer.write_table()
        writer.close()
        return"成功"
    
    except:
        return"写入文件失败"

def main():
    
    articul_id=[]
    articul_infos=[]
    count=0
    pages=range(1,2)
    
    for page in pages:
        url="http://www.shxyj.org/Magazine?Year=&Issue=&Title=&Keywords=&WorkUnit=&page="+str(page)
        html=gethtml(url)
        articul_id=get_id(articul_id,html)
    
    articul_infos=get_info(articul_infos,articul_id,count)
        
    articul_info=into_file(articul_infos)
    
    print("已成功保存")
       
main()