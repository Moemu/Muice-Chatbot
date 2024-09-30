from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt

class AutoPrompt:
    default_commands = []

    @classmethod
    def load_commands(cls, default_commands: dict):
        cls.commands = []
        for command, function in default_commands.items():
            cls.commands.append(command)
        cls.completer = WordCompleter(
            cls.commands,
            ignore_case=True,
        )

    @classmethod
    def prompt(cls):
        text = prompt(
            ">>>",
            completer=cls.completer,
            complete_style=CompleteStyle.MULTI_COLUMN,
        )
        return text

