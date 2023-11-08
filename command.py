import os,shutil

class Command():
    '''
    指令类
    '''
    def __init__(self,Muice):
        self.commands = []
        self.commands_function = []
        self.Muice = Muice
        
    def resister_command(self,command:str,command_function):
        '''
        注册命令
        Args:
            command: 命令字符串
            command_function: 所执行的函数
        '''
        self.commands.append(command)
        self.commands_function.append(command_function)

    def run(self,command:str) -> (bool,str):
        '''
        执行命令，返回命令是否存在的布尔值，以及命令执行结果或源字符串
        '''
        for i in range(len(self.commands)):
            if self.commands[i] == command:
                return True,self.commands_function[i]()
        return False,command

    def load_default_command(self):
        '''
        加载默认命令
        '''
        self.resister_command('/help',self.default_help)
        self.resister_command('/refresh',self.refresh)
        self.resister_command('/clean',self.clean)
        self.resister_command('/reset',self.reset)
        self.resister_command('/undo',self.undo)
        
    def default_help(self):
        help_text = "/clean 清空本轮对话历史 \n /help 显示所有可用的命令列表 \n /refresh 刷新本次对话回复 \n /reset 重置所有对话数据(将存档对话数据) \n /undo 撤销上一次对话"
        return help_text
    
    def refresh(self):
        reply = self.Muice.refresh()
        self.Muice.save_chat_memory(reply)
        return reply
    
    def clean(self):
        self.Muice.history = []
        return ''
    
    def reset(self):
        shutil.copy(f'./memory/{self.Muice.user_qq}.json','./memory/chat_memory_backup.json')
        os.remove(f'./memory/{self.Muice.user_qq}.json')
        self.Muice.history = []
        return ''
    
    def undo(self):
        self.Muice.remove_last_chat_memory()
        self.Muice.history = self.Muice.get_recent_chat_memory()
        return ''