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
    return x.json()

if __name__ == "__main__":
    dir = os.getcwd()
    os.chdir(dir)
    print (dir)

    if not os.path.isdir("src"): os.mkdir("src")

    if not os.path.isfile(os.path.join(dir, "src", "eula.txt")):
        with open(os.path.join(dir, "src", "eula.txt"), 'w') as file:
            file.write("eula=true")

    if not os.path.isfile("start.bat"):
        with open(os.path.join(dir,"start.bat"), 'w') as file:
            file.write(F"python3 \"{dir}\{os.path.basename(__file__)}\"")

    vers=dl_json('https://papermc.io/api/v2/projects/paper')["versions"][-1]
    print(vers)
    build=dl_json('https://papermc.io/api/v2/projects/paper/versions/'+vers)['builds'][-1]
    print(build)
    dwnld=dl_json('https://papermc.io/api/v2/projects/paper/versions/'+vers+'/builds/'+str(build))["downloads"]['application']
    print(dwnld)
    if not os.path.isfile(os.path.join(dir, "src", dwnld['name'])): dl_file(F'https://papermc.io/api/v2/projects/paper/versions/{vers}/builds/{str(build)}/downloads/{dwnld["name"]}', dwnld['name'], path=os.path.join(dir, "src"))
    os.chdir(os.path.join(dir, "src"))
    os.system(F"java -jar \"{dir}\src\{dwnld['name']}\" nogui")
    sys.exit()
