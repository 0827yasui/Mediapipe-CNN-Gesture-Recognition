import yaml

class YAML_READ():
    def __init__(self):
        pass

    def Set_Yaml(self, file_name):
        with open(file_name, "r", encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data
    
    def Get_value(self, data, label_name):
        value = data
        for name in label_name:
            value = value[name]
        return value
