import requests


def prmess( prid , messages , post ):
   '''
   发送私聊消息
   '''
   url = "http://127.0.0.1:"+str(post)+"/send_private_msg"                      
   headers = {"content-type":"application/json",'Connection':'close'}
   mess = {"user_id":prid,"message":messages}
   res = requests.post(url, json = mess,headers=headers)
   return(res.text)



#prmess(prid=2236319712,messages="启动",post="6542")     #测试使用