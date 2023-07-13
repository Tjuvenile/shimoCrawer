import requests,json

cookie = ""
userAgent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
header = {"User-Agent": userAgent.encode("UTF-8"), "cookie": cookie.encode("UTF-8"),
          "content-type": "application/json;charset=UTF-8", "referer": "https://shimo.im/desktop"}
urlPath = "https://shimo.im/lizard-api/"

def main():
    # 本空间 ： 要移动到的空间
    list = [{"25q5Mbx90pswMoqD": "gXqmdBLyLBfyOa3o"}]
    i = 0
    while len(list) > 0:
        item = list[0].popitem()
        url = "https://shimo.im/lizard-api/files?folder=" + item[0]
        req = requests.get(url=url, headers=header)
        reqJson = json.loads(s=req.text)
        for data in reqJson:
            i += 1
            # 是文件
            if data["is_folder"] == 0:
                moveFile(data["guid"], data["name"], item[1])
                pass
            else:  # 是文件夹
                dirguid = mkdir(data["name"], item[1])
                list.append({data["guid"]:dirguid})
            print("第" + str(i) + "个文件,name: " + data["name"])
        list.pop(0)

# 移动文件夹
def moveFile(currentFileGuid, copyName, folder):
    # 复制一个文件到我的空间
    url = urlPath + "files/action/duplicate"
    dictFile = {"files":[{"guid":currentFileGuid,"name":copyName}],"folder":folder}
    text = json.dumps(dictFile).encode("UTF-8")
    requests.post(url=url,data=text, headers=header)

# 创建文件夹
def mkdir(name, folder):
    url = urlPath + "files"
    dictFile = {"type": "folder", "name": name, "folder": folder}
    text = json.dumps(dictFile).encode("UTF-8")
    req = requests.post(url=url, data=text, headers=header)
    return json.loads(s=req.text)["guid"]

if __name__ == "__main__":
    main()
