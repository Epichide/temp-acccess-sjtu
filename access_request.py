
import requests
import os.path as osp
import yaml
from utils import *
import argparse
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#==============Param=================================
param = {   
    'campus': "闵行校区",
    'time': 2,
    'xm': "your name",
    'zjhm': "your id number",
    'phone': "your phonenumber",
    'iknow': 1,
    }


# 发件人邮箱地址
sendAddress = 'xxx@126.com'
# 发件人授权码
password = 'xxxxxxxxxxxxxx'

#====================================================

def get_parser():
    parser = argparse.ArgumentParser(description="* Auto Report Installer *")
    parser.add_argument('-n', '--name', help='your name')
    parser.add_argument('-i', '--id', help='your id')
    parser.add_argument('-p', '--phone', help='your phone')
    parser.add_argument('-e', '--email', help='your receive email address')
    parser.add_argument('-au', '--authorization', help='your receive email authorization code')
    parser.add_argument('-l', '--log', help='whether to log',default=False,action='store_true')
    return parser


def generate_email_body(server,msg, email_to_list, email_title, email_content, attchment_path=None, files=[]):
    """
    组成邮件体
    :param email_to_list:收件人列表
    :param email_title:邮件标题
    :param email_content:邮件正文内容
    :param attchment_path:附件的路径
    :param files:附件文件名列表
    :return:
    """
    msg['Subject'] = email_title
    msg['From'] = "我"
    msg['To'] = ",".join(email_to_list)

    for file in files:
        file_path = attchment_path + '/' + file
        if os.path.isfile(file_path):
            # 构建一个附件对象
            att = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att.add_header("Content-Disposition", "attachment", filename=("gbk", "", file))
            msg.attach(att)

    text_plain = MIMEText(email_content, 'plain', 'utf-8')
    msg.attach(text_plain)
    #authorization code
    server.sendmail(sendAddress,email_to_list,msg.as_string())
    print('发送成功')




def main():
     
    parser = get_parser()
    args = parser.parse_args()    
    global sendAddress
    global password 
    if args.name:
        param["xm"]=args.name  
    if args.name:
        param["phone"]=args.phone  
    if args.name:
        param["zjhm"]=args.id  
    if args.email:
        
        sendAddress=args.email
        idx=sendAddress.find("@")
        # 连接服务器
        server = smtplib.SMTP_SSL('smtp.'+sendAddress[idx+1:], 465)
        """
        邮箱	    服务器
        新浪邮箱	http://smtp.sina.com
        搜狐邮箱	http://smtp.sohu.com
        126邮箱	    http://smtp.126.com
        QQ邮箱	    http://smtp.qq.com
        163邮箱	    http://smtp.163.com
        """
    else:
        # 连接服务器
        server = smtplib.SMTP_SSL('smtp.126.com', 465)
  
    if  args.authorization:
        password=args.authorization
    
    logger = Logger.get_logger()
    logger.enable=False
    if args.log:
        logger.enable=args.log
    def wlog(logger,message):
        if logger.enable:
            logger.info(message)
    # campus login wibsite
    website={
        "闵行校区":"https://sjtu.cn/vreg/mh",
        "徐汇校区":"https://sjtu.cn/vreg/xh"   
    }
    #--------------------------------------------------------------     
    
       
    path = os.path.split(os.path.realpath(__file__))[0]
    # create the task
    with open(osp.join(path, "etc/shjt.yaml"), encoding="utf-8") as f:
        headers = yaml.load(f,Loader=yaml.FullLoader)  # 将文件的内容转换为字典形式


    session = requests.session()
    session.trust_env = False
    logger.debug('apply for accession today')
    response= session.post(website[param["campus"]])
    response= session.post(response.url)
    response= session.post(response.url)
    response= session.post(response.url)
    headers["Cookie"]="VISITOR="+str(session.cookies.get_dict()["VISITOR"])
    session.headers.update(headers)
    response = session.post("https://qiandao.sjtu.edu.cn/visitor/submit.php", data=param)
    
    pain_text=""
    pain_text+="cookie: "+headers["Cookie"]+"\n"
    
    status="成功" if "成功" in response.text else "失败"
    pain_text+="下午申请状态："+status+"\n"
  
    if "成功" not in response.text:
        pain_text+=response.text+"\n"
        
    param["time"]=1
    response = session.post("https://qiandao.sjtu.edu.cn/visitor/submit.php", data=param)
    status="成功" if "成功" in response.text else "失败"

    pain_text+="上午申请状态："+status+"\n"
    if "成功" not in response.text:
        pain_text+=response.text+"\n"
        

    # 登录邮箱
    try:
        loginResult = server.login(sendAddress, password)
    except Exception as e:
        print(e)
        logger.info(pain_text)
        raise
    if "successful" not in str(loginResult[1]):
        print(loginResult)
        logger.info(pain_text)
        raise
   
    msg = MIMEMultipart()
    generate_email_body(server,msg, [sendAddress], "daily access application status", pain_text)
    wlog(logger,pain_text)
    
    # print(response.text)

    #print("状态：","成功" in response.text)
if __name__=="__main__":
    main()

