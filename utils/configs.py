import yaml

def get() -> dict:
    configs = yaml.load(open('configs.yml', 'r', encoding='utf-8'),Loader=yaml.FullLoader)
    if configs['bot']['platform'] == 'telegram':
        configs['bot']['cq_code'] = True
        configs['bot']['group']['enable'] = True
        configs['bot']['group']['anyone'] = True
        configs['bot']['group']['only_at'] = False
        configs['bot']['group']['rate'] = 100
    return configs