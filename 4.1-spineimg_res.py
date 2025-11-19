import base64
import argparse
import os
import sys
import json
import subprocess


atlasDir = './allatlas'

resMapfile = "./0-resmap.json"
spineResJson = None
spineName2IdDic = None
spineId2ImgDic = None


def findImg(search_string, dirCount):
    if search_string == "":
        return

    search_string = "*" + search_string + "*"
    result = subprocess.run(["find", atlasDir, "-name", search_string], stdout=subprocess.PIPE)
    outstr = result.stdout.decode('utf-8')
    lines = outstr.split("\n")
    checkOneTime = {}
    for line in lines:
        data = line.split("/")
        if len(data) < 2:
            continue

        dir = data[len(data) - 2]
        if dir in checkOneTime:
            continue

        checkOneTime[dir] = 1
        if dir not in dirCount:
            dirCount[dir] = 1
        else:
            dirCount[dir] +=1


def calcSpineImgMostUseDir(spine):
    filePath = "./allspine/{0}/{0}.txt".format(spine)
    if not os.path.exists(filePath):
        print("not found spine txt file: ", filePath)
    
    dirCount = {}

    with open(filePath, 'r') as file:
        for line in file:
            findImg(line.strip(), dirCount)

    maxCount = 0
    if len(dirCount) > 0:
        max_key = max(dirCount, key=dirCount.get)
        for info in dirCount:
            if dirCount[info] >= maxCount:
                maxCount = dirCount[info]
                max_key = info

        if spine in spineName2IdDic:
            spineid = spineName2IdDic[spine]
            if not spineid in spineId2ImgDic:
                spineId2ImgDic[spineid] = []
            if max_key not in spineId2ImgDic[spineid]:
                arr = spineId2ImgDic[spineid]
                spineId2ImgDic[spineid].append(max_key)
                print("add spine img: ", spine, max_key)


if __name__ == '__main__':
    json_str = open(resMapfile, 'r').read()
    spineResJson = json.loads(json_str)
    spineName2IdDic = spineResJson['name2id']
    spineId2ImgDic = spineResJson['id2img']
    
    # calcSpineImgMostUseDir("gool_bigwin_SkeletonData")
    
    result = subprocess.run(["ls", "./allspine"], stdout=subprocess.PIPE)
    outstr = result.stdout.decode('utf-8')
    lines = outstr.split("\n")
    for line in lines:
        if len(line) < 1:
            continue
        
        calcSpineImgMostUseDir(line)

    json_str = json.dumps(spineResJson, indent=4)
    with open(resMapfile, "w") as file:
        file.write(json_str)

    print('end')