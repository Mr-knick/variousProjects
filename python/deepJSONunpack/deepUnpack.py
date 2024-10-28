
packagedDict = {
    'pre' :
        {
            1: 'Step one',
            2: 'Step two',
            3: 'Step three'
        },
    'stages':
        {
            1: "db call",
            2: {"single file": "Do This With One File",
                "multi file": {
                    0: {
                        "loop instruction": True
                    },
                    1: "Press button on device",
                    2: "Do this with each file"
                }
                },
            3: "port call",
            4: {"single file": "Do This With One File",
                "multi file": "Do this for multi files"
                }
        },
    'post': 'db save'
}

singleFile = True

print(packagedDict)
preItems = packagedDict['pre'].keys()
for x in sorted(preItems):
    print(packagedDict['pre'][x])

stagesItems = packagedDict['stages'].keys()
for x in sorted(stagesItems):
    if x==1:
        print(packagedDict['stages'][1])
    if x==2:
        if(singleFile):
            print(packagedDict['stages'][x]['single file'])
        else:
            multiFileItems = packagedDict['stages'][x]['multi file'].items()
            for y in sorted(multiFileItems):
                print(packagedDict['stages'][x]['multi file'][y])

print(packagedDict['post'])