import os,shutil,sys

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

    def run(self,command:str) -> str:
        '''
        执行命令，返回命令命令执行结果或命令不存在的提示
        '''
        for i in range(len(self.commands)):
            if self.commands[i] == command:
                return self.commands_function[i]()
        return self.no_command()
    
    def no_command(self):
        return "没有当前命令"
    #用于后期其他功能扩展

    def load_default_command(self):
        '''
        加载默认命令
        '''
        self.resister_command('/help',self.default_help)
        self.resister_command('/refresh',self.refresh)
        self.resister_command('/clean',self.clean)
        self.resister_command('/reset',self.reset)
        self.resister_command('/undo',self.undo)
        self.resister_command('/restart',self.restart)
        
    def default_help(self):
        help_text = "/clean 清空本轮对话历史 \n /help 显示所有可用的命令列表 \n /refresh 刷新本次对话回复 \n /reset 重置所有对话数据(将存档对话数据) \n /undo 撤销上一次对话"
        return help_text
    
    def refresh(self):
        reply = self.Muice.refresh()
        self.Muice.save_chat_memory(reply)
        return reply
    
    def clean(self):
        self.Muice.history = []
        return "cleaned"
    
    def reset(self):
        shutil.copy(f'./memory/{self.Muice.user_qq}.json','./memory/chat_memory_backup.json')
        os.remove(f'./memory/{self.Muice.user_qq}.json')
        self.Muice.history = []
        return "reseted"
    
    def undo(self):
        self.Muice.remove_last_chat_memory()
        self.Muice.history = self.Muice.get_recent_chat_memory()
        return "undoed"
    
    
    def restart(self):
        print("restarting...")
        current_script = sys.argv[0]
        # 使用os.execv来替换当前进程并重新执行main.py
        # 注意：这将导致当前方法的剩余部分不会被执行
        #os.execv(sys.executable, [sys.executable, current_script] + sys.argv[1:])
        #重启逻辑,或许会有
        return "restart"

    
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