import requests



def prmess(  prid , messages , send_post ):
    '''发送私聊消息'''
    url = "http://127.0.0.1:"+str(send_post)+"/send_private_msg"                      
    headers = {"content-type":"application/json",'Connection':'close'}
    mess = {"user_id":prid,"message":messages}
    res = requests.post(url, json = mess,headers=headers)
    return(res.text)
    

def prAudio( prid , messages , send_post ):
    '''发送私聊语音消息'''
    messages = {"type": "record","data": {"file": "base64://"+messages}}
    url = "http://127.0.0.1:"+str(send_post)+"/send_private_msg"                      
    headers = {"content-type":"application/json",'Connection':'close'}
    mess = {"user_id":prid,"message":messages}
    res = requests.post(url, json = mess,headers=headers)
    return(res.text)

#base64 = 
#print(prAudio(2236319712,base64,6542))
#print(prAudio(2307804249,base64,1235))