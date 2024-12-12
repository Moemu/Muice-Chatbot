import os
import shutil
import logging

import threading
from utils.auto_prompt import AutoPrompt

logger = logging.getLogger('Muice')

class Command:
    """
    指令类
    """

    def __init__(self, muice):
        self.Muice = muice
        self.commands = {}

    def register_command(self, command: str, command_function):
        """
        注册命令
        Args:
            command: 命令字符串
            command_function: 所执行的函数
        """
        self.commands[command] = command_function

    def run(self, command: str) -> str:
        """
        执行命令，返回命令命令执行结果或命令不存在的提示
        """
        logger.info(f"捕获到命令：{command}")
        if command in self.commands:
            # 调用与命令关联的函数
            return self.commands[command]()
        logger.warning(f"未找到命令：{command}")
        return self.no_command()

    def no_command(self) -> str:
        return "没有这样的命令呢"

    # 用于后期其他功能扩展

    def load_default_command(self):
        """
        加载默认命令
        """
        default_commands = {
            '/help': self.default_help,
            '/refresh': self.refresh,
            '/clean': self.clean,
            '/reset': self.reset,
            '/undo': self.undo
        }
        for command, function in default_commands.items():
            self.register_command(command, function)
        threading.Thread(target=self.command_thread, args=(default_commands,)).start()

    def default_help(self):
        help_text = ("/clean 清空本轮对话历史 \n "
                     "/help 显示所有可用的命令列表 \n "
                     "/refresh 刷新本次对话回复 \n "
                     "/reset 重置所有对话数据(将存档对话数据) \n "
                     "/undo 撤销上一次对话")
        return help_text

    def refresh(self) -> str:
        reply = self.Muice.refresh()
        self.Muice.save_chat_memory(reply)
        return reply

    def clean(self) -> str:
        self.Muice.history = []
        return "已成功重置对话上下文~"

    def reset(self) -> str:
        memory_file = self.Muice.user_id
        if os.path.isfile(f'./memory/{memory_file}_backup.json'):
            os.remove(f'./memory/{memory_file}_backup.json')
        if not os.path.isfile(f'./memory/{memory_file}.json'):
            return "指令执行失败：我没有和你说过一句话哦"
        shutil.copy(f'./memory/{memory_file}.json', f'./memory/{memory_file}_backup.json')
        os.remove(f'./memory/{memory_file}.json')
        self.Muice.history = []
        return "已成功移除记忆~"

    def undo(self) -> str:
        self.Muice.remove_last_chat_memory()
        self.Muice.history = self.Muice.get_recent_chat_memory()
        return "已成功撤销上一段对话~"

    def command_thread(self, commands):
        AutoPrompt.load_commands(commands)
        try:
            while True:
                im_text = AutoPrompt.prompt()
                response = self.run(im_text)
                print(response)
        except KeyboardInterrupt:
            pass