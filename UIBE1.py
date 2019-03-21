#!C:\Users\NickyChu\AppData\Local\Programs\Python
# coding: utf-8
# author: NickyChu

import tkinter
import requests
from bs4 import BeautifulSoup
from random import randint
import time
import os
import queue
import sys

nicky = tkinter.Tk()
nicky.title("UIBE课件下载工具@author:NickyChu")
nicky.geometry("1300x380+300+150")


# add image
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
canvas = tkinter.Canvas(nicky)
imageDirection = "D:"
image_file = tkinter.PhotoImage(file=resource_path(os.path.join(imageDirection, 'rick.png')))
image = canvas.create_image(0,0,anchor='nw',image=image_file)
canvas.place(x=0,y=0,height=360, width=619)

# add lable_title
lp_title = tkinter.Label(nicky,text='UIBE课件下载工具',font=("微软雅黑",20),fg='#32cd99')
lp_title.place(x=625,y=50)

# add copyright_lable
copyright_lable = tkinter.Label(nicky,text='NickyChu @ copyright 2019   Email Address: clr0521@163.com')
copyright_lable.pack(side='bottom')

# add name
name_text = tkinter.Variable()
name_lb = tkinter.Label(nicky,text='用户名：',font=('微软雅黑',12))
name_lb.place(x=630,y=120)
name_input = tkinter.Entry(nicky,textvariable=name_text,width=20)
name_input.place(x=700,y=120)

# add password
pwd_text = tkinter.Variable()
pwd_lb = tkinter.Label(nicky,text='密码：',font=('微软雅黑',12))
pwd_lb.place(x=630,y=160)
pwd_input = tkinter.Entry(nicky,show="*",width=20,textvariable=pwd_text)
pwd_input.place(x=700,y=160)
#add 课件选择
choose_text = tkinter.Variable()
choose_lb = tkinter.Label(nicky,text='序号：',font=('微软雅黑',12))
choose_lb.place(x=630,y=200)
choose_input = tkinter.Entry(nicky,width=20,textvariable=choose_text)
choose_input.place(x=700,y=200)

# username  and password is real
def loginjwc():
    '''
    登陆教务处系统并返回req对象
    '''
    import requests
    from bs4 import BeautifulSoup
    from random import randint
    import queue
    
    account=name_text.get()
    password=pwd_text.get()
    url = 'http://tas1.uibe.edu.cn:81'

    headers = {
        "Host": "tas1.uibe.edu.cn:81",
        "Connection": "keep-alive",
        "Content-Length": "349",
        "Cache-Control": "max-age=0",
        "Origin": "http://tas1.uibe.edu.cn:81",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://tas1.uibe.edu.cn:81/Account/Login.aspx",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    headers1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    }
    global req 
    req = requests.Session()
    html = req.get(url,headers=headers1).text
    bs = BeautifulSoup(html,'html.parser')
    _VIEWSTATE = bs.find_all('input',type='hidden')[0]['value']
    _VIEWSTATEGENERATOR = bs.find_all('input',type='hidden')[1]['value']
    cookies = {"ASP.NET_SessionId":req.cookies["ASP.NET_SessionId"]}
    
    data = {
        "txtName": account,
        "txtPassword": password,
        "__VIEWSTATE": _VIEWSTATE,
        "__VIEWSTATEGENERATOR": _VIEWSTATEGENERATOR,
        "ddlLevel": "2",
        "ibtnLogin.x": str(randint(1,50)),
        "ibtnLogin.y": str(randint(1,50))
    }
    url1 = 'http://tas1.uibe.edu.cn:81/Account/Login.aspx'
    response = req.post(url=url1, data=data, headers=headers, cookies = cookies)
    html = response.text
    cj = requests.cookies.RequestsCookieJar()
    cj.set("ASP.NET_SessionId", cookies["ASP.NET_SessionId"])
    req.cookies=cj
    req.header = headers
    if  "对外经济贸易大学教学辅助平台" in html:   
        t.insert("end",'登陆成功')
        #获取课程
        soup = BeautifulSoup(html,features='html.parser')
        links = soup.find("table",id = "dlstList").find_all('a')
        linklst = []
        global course_name
        course_name = []
        for link in links:
            linklst.append(link["href"])
            course_name.append(link["title"].split("（")[0])
        #这里需要改进为一个函数
        urlstart = "http://tas1.uibe.edu.cn:81/CourseNotice/ClassNoticeList.aspx?ClassID="
        import re
        def plusurl(url1,url2):
            return url1+url2
        linknw = [plusurl(urlstart,re.findall("\d+",link)[0]) for link in linklst]
        #得到所有的课程id
        global class_id
        class_id = [link.split("ClassID=")[1] for link in linknw]
        global class_slides_url_head
        class_slides_url_head = 'http://tas1.uibe.edu.cn:81/CourseWare/ClassCourseWareList.aspx?ClassID='
        global class_slides_url 
        class_slides_url = [class_slides_url_head+i for i in class_id]
        t.insert("end",("\n——————— 课程选择菜单 —————————\n"))
        for i in range(len(class_id)):
            t.insert("end",("序号{0}.\t课程名:{1}(ID={2})\n".format(i,course_name[i],class_id[i])))
        t.insert("end","\n—— 请在序号栏输入想批量下载课件的课程序号 ——\n")
        t.insert("end"," (PS:请用空格进行分隔,输入all则全部下载)")
        t.see(tkinter.END)
        t.update()
    else:
        t.insert('end',"登陆失败")
        
#得到该课程的课件url
def getslide_link(req,link):
    data = {
        "__EVENTTARGET": "dgdList$ctl14$ctl01",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE":""
    }
    in_flag = True
    slide_link = []
    name = []
    name1 = []
    count_page = 0
    html = req.get(link).text
    while(in_flag):
        url_head = "http://tas1.uibe.edu.cn:81"
        time.sleep(1)
        count_page = count_page+1
        soup2 = BeautifulSoup(html,'html.parser').find("table",{"class":"data"})
        soup3 = soup2.find_all("a")
        for sp in soup3:
            time.sleep(1)
            href = sp["href"].strip("..")
            nm = sp.string
            name1.append(nm)
            if "javascript" not in href:
                slide_link.append(url_head+href)
                name.append(nm)
        if name1[-1] == "下一页":
            t.insert("end",("获取第{}页链接\n".format(count_page)))
            t.see(tkinter.END)
            t.update()
            html = req.post(link,data=data).text
        else:
            in_flag = False

    return slide_link,name

#抓取当前页面的课件

def slide_downloader(req,slide_link_1,name_1,course_name,filepath):
    t.insert("end",("\n-------Start Downloading With Requests-------\n"))
    for i in range(len(slide_link_1)):
        #注意先定义filename，正确定义文件名称很关键
        filename = filepath +"/"+ name_1[i] +"."+ slide_link_1[i].split('.')[-1]
        #检查文件是否存在
        if os.path.exists(filename):
            t.insert("end",(name_1[i]+"\t已经存在\n"))
        else:
            #正式下载
            time.sleep(1)
            t.insert("end",("正在下载:"+filename+"\n"))
            t.see(tkinter.END)
            t.update()
            r1 = req.get(slide_link_1[i],stream=True)
            data = r1.content
            with open(filename, "wb") as file:
                file.write(data)
            #with open(filename, "wb") as code:
           #      code.write(r1.content)
           
    t.insert("end",("\n-----------下载完成!-------------\n"))
        
#下载按钮触发
def download():
    #处理课程选择
    class_choose = choose_text.get()
    class_id_choose = []
    class_slides_url_choose = []
    class_names_choose = []
     #处理输入数据
    if class_choose == 'all':
        class_choose = range(len(class_id))
    else:
        class_choose = class_choose.split(" ")
        #检查数据正确性
    t.delete('1.0','end')
    for i in class_choose:
        q = int(i)
        if q not in range(len(class_id)):
            t.insert("end",("格式有误，请重新输入!"))
            in_flag = False
            break
        else:   
            class_id_choose.append(class_id[int(i)])
            class_slides_url_choose.append(class_slides_url[int(i)])
            class_names_choose.append(course_name[int(i)])
            in_flag = True
    if in_flag == True:
        for i in range(len(class_id_choose)):
            filepath = 'D:/UIBE_Slides/'+ class_names_choose[i]
            slide_link_1,name_1 = getslide_link(req,class_slides_url_choose[i])
            if os.path.exists(filepath):
                slide_downloader(req,slide_link_1,name_1,class_names_choose[i],filepath)
            else:
                os.makedirs(filepath)
                #创建文件目录
                slide_downloader(req,slide_link_1,name_1,class_names_choose[i],filepath)




# add login_button
login_button = tkinter.Button(nicky,text='登陆',font=('微软雅黑',12),command=loginjwc)
login_button.place(x=730,y=240)

# add quit_button
quit_button = tkinter.Button(nicky,text='退出',font=('微软雅黑',12),command=nicky.quit)
quit_button.place(x=660,y=240)
# add quit_button
download_button = tkinter.Button(nicky,text='下载',font=('微软雅黑',12),command=download)
download_button.place(x=800,y=240)

#text显示信息
t = tkinter.Text(nicky,width=50,height=23)
t.place(x=900,y=30)
nicky.mainloop()
