import yaml as yaml_
import shutil
import sys
from pathlib import Path
from ruamel.yaml import YAML
from .logging import init_logger


TEMPLATE_PATH = Path(__file__).parent / "configs_template.yml"
CONFIG_PATH = Path("configs.yml").resolve()
yaml = YAML()
logger = init_logger()

def copy_config(TEMPLATE_PATH, CONFIG_PATH):
    """
    复制模板配置文件到config
    """
    shutil.copy(TEMPLATE_PATH, CONFIG_PATH)

def get_all_keys(d, parent_key=''):
    keys = set()
    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            keys.update(get_all_keys(v, new_key))
        else:
            keys.add(new_key)
    return keys

def check_yaml_is_changed(TEMPLATE_PATH):
    """
    检查配置文件是否需要更新
    """
    with open("configs.yml", "r", encoding="utf-8") as f:
        old = yaml_.load(f, Loader=yaml_.FullLoader)
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        example_ = yaml_.load(f, Loader=yaml_.FullLoader)
    
    keys1 = get_all_keys(example_)
    keys2 = get_all_keys(old)

    # 忽略 model 下的所有子配置项变化
    keys1 = {k for k in keys1 if not k.startswith("model.")}
    keys2 = {k for k in keys2 if not k.startswith("model.")}
    
    return keys1 != keys2

def merge_configs(old_config, new_config):
    """
    合并配置文件
    """
    for key, value in new_config.items():
        if key in old_config:
            if isinstance(value, dict) and isinstance(old_config[key], dict):
                merge_configs(old_config[key], value)
        else:
            logger.info(f"新增配置项: {key} = {value}")
            old_config[key] = value
    return old_config

def update_config(func):
    def wrapper(*args, **kwargs):
        if not CONFIG_PATH.exists():
            logger.warning("配置文件不存在,正在创建")
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            copy_config(TEMPLATE_PATH, CONFIG_PATH)
            logger.info("请在configs.yml中配置相关信息")
            sys.exit(1)
        else:
            logger.info("配置文件存在,正在读取")

            if check_yaml_is_changed(TEMPLATE_PATH):
                yaml_2 = YAML()
                logger.info("配置文件已更新到新的版本, 正在合并")

                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    old_config = yaml_2.load(f)

                with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
                    new_config = yaml_2.load(f)

                merged_config = merge_configs(old_config, new_config)

                with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                    yaml_2.dump(merged_config, f)

        # with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        #     yaml_config = yaml_.load(f, Loader=yaml_.FullLoader)

        return func(*args, **kwargs)
    return wrapper

@update_config
def get() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        configs = yaml_.load(f, Loader=yaml_.FullLoader)
    
    if configs['bot']['platform'] == 'telegram':
        configs['bot']['cq_code'] = True
        configs['bot']['group']['enable'] = True
        configs['bot']['group']['anyone'] = True
        configs['bot']['group']['only_at'] = False
        configs['bot']['group']['rate'] = 100
    
    return configs