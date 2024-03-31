import requests


def prmess( prid , messages , port ):

   url = "http://127.0.0.1:"+str(port)+"/send_private_msg"                      

   headers = {"content-type":"application/json",'Connection':'close'}

   mess = {"user_id":prid,"message":messages}


   res = requests.post(url, json = mess,headers=headers)

   #print (res.text)
   return(res.text)



#prmess(prid=2236319712,messages="a",port="8010")     #测试使用
