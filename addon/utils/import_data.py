import json
import codecs

def import_data(input_path: str) -> list:
    data_format = input_path.split('.')[-1]
    data = []
    if data_format == 'json': 
        data = codecs.open(
            input_path, 'r', encoding='utf-8'
        ).read()

        json_data = json.loads(data)
    return json_data['shapes']
