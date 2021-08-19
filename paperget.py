import os, sys, requests, json

def dl_file(url, filename, path=''):
    headers = requests.utils.default_headers()
    x = requests.get(url, headers=headers)
    if path=='':
        with open(filename, 'wb') as file:
            file.write(x.content); file.close()
    else:
        if not os.path.isdir(path): os.makedirs(path)
        with open(os.path.join(path,filename), 'wb') as file:
            file.write(x.content); file.close()

def dl_json(url):
    x = requests.get(url, headers=requests.utils.default_headers())
    return json.loads((x.text))
if __name__ == "__main__":
    vers=dl_json('https://papermc.io/api/v2/projects/paper')["versions"][-1]
    print(vers)
    build=dl_json('https://papermc.io/api//v2/projects/paper/versions/'+vers)['builds'][-1]
    print(build)
    dwnld=dl_json('https://papermc.io/api//v2/projects/paper/versions/'+vers+'/builds/'+str(build))["downloads"]['application']
    print(dwnld)
    dl_file('https://papermc.io/api//v2/projects/paper/versions/'+vers+'/builds/'+str(build)+'/downloads/'+dwnld['name'], dwnld['name'])
