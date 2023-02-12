import json


def test_save_links():
    file_path = 'links.json'
    urls = ['olo', 'mnat']
    with open(file_path, 'r') as f:
        data = json.load(f)
        data['links'].extend(urls)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
