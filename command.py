import os,shutil,sys

class Command():
    '''
    指令类
    '''
    def __init__(self,Muice):
        self.Muice = Muice

    def no_command(self):
        return "没有当前命令"
    #用于后期其他功能扩展

    def default_help(self,mess_self):
        help_text = " /clean 清空本轮对话历史 \n /help 显示所有可用的命令列表 \n /refresh 刷新本次对话回复 \n /reset 重置所有对话数据(将存档对话数据) \n /undo 撤销上一次对话"
        return help_text
    
    def refresh(self,mess_self):
        reply = self.Muice.refresh()
        self.Muice.save_chat_memory(reply)
        return reply
    
    def clean(self,mess_self):
        self.Muice.history = []
        return "cleaned"
    
    def reset(self,mess_self):
        shutil.copy(f'./memory/{self.Muice.user_qq}.json','./memory/chat_memory_backup.json')
        os.remove(f'./memory/{self.Muice.user_qq}.json')
        self.Muice.history = []
        return "reseted"
    
    def undo(self,mess_self):
        self.Muice.remove_last_chat_memory()
        self.Muice.history = self.Muice.get_recent_chat_memory()
        return "undoed"
    
    
    def restart(self,mess_self):
        print("restarting...")
        current_script = sys.argv[0]
        # 使用os.execv来替换当前进程并重新执行main.py
        # 注意：这将导致当前方法的剩余部分不会被执行
        #os.execv(sys.executable, [sys.executable, current_script] + sys.argv[1:])
        #重启逻辑,或许会有
        return "restart"
    
    def echo(self,mess_self):
        content = mess_self.mess[6:]
        return content

    
    def execute(self, command: str) -> str:
        '''
        执行命令或返回指定文本
        Args:
            command: 要执行的命令字符串
        Returns:
            如果命令存在并执行成功，返回文本"b"，否则返回文本"a"
        '''
        is_command,result = self.run(command)
        if result[0]:  # 如果命令存在
            # 执行命令并返回结果
            return result[1]()  # 执行命令对应的函数
        else:
            # 命令不存在，返回"a"
            return "未知命令"