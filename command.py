import os
import shutil
import logging


def no_command():
    data = "没有当前命令"
    return {f"data": [{data}], "type": "msg"}


class Command:
    """
    指令类
    """

    def __init__(self, muice):
        self.Muice = None
        self.commands = {}
        self.raw_data_command_list = []  # list类型 需要rawdata的自取

        self.load_default_command()

    def register_command(self, command: str, command_function):
        """
        注册命令
        Args:
            command: 命令字符串
            command_function: 所执行的函数
        """
        self.commands[command] = command_function


    def run(self, command: str, raw_data, message) -> dict[str, list[str] | str]:
        """
        执行命令，返回命令命令执行结果或命令不存在的提示
        """
        logging.debug(f"运行指令: {command}")
        if command in self.commands:
            if command in self.raw_data_command_list:
                return self.commands[command](raw_data)
            return self.commands[command](message)
        return no_command()

    def load_default_command(self):
        """
        加载默认命令
        """
        default_commands = {
            'help': self.default_help,
            'refresh': self.refresh,
            'clean': self.clean,
            'reset': self.reset,
            'undo': self.undo,
        }
        for command, function, in default_commands.items():
            self.register_command(command, function)

    def default_help(self, message):
        help_text = ("/clean 清空本轮对话历史 \n "
                     "/help 显示所有可用的命令列表 \n "
                     "/refresh 刷新本次对话回复 \n "
                     "/reset 重置所有对话数据(将存档对话数据) \n "
                     "/undo 撤销上一次对话")
        return {"data": [help_text], "type": "msg"}

    def refresh(self, message):
        reply = self.Muice.refresh()
        self.Muice.save_chat_memory(reply)
        return {"data": [reply], "type": "msg"}

    def clean(self, message):
        self.Muice.history = []
        return {"data": ["cleaned"], "type": "msg"}

    def reset(self, message):
        shutil.copy(f'./memory/{self.Muice.user_id}.json', './memory/chat_memory_backup.json')
        os.remove(f'./memory/{self.Muice.user_id}.json')
        self.Muice.history = []
        return {"data": ["reseted"], "type": "msg"}

    def undo(self, message):
        self.Muice.remove_last_chat_memory()
        self.Muice.history = self.Muice.get_recent_chat_memory()
        return {"data": ["undoed"], "type": "msg"}
