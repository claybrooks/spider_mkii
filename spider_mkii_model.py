import lxml.etree as et

def parseXml(xmlFilePath):

    try:
        with open(xmlFilePath, 'r') as f:
            fxBanks = et.parse(f).getroot()
    except Exception as e:
        print (e)
        return

    toReturn = {}

    for fxBank in fxBanks.iter('FxBank'):
        id = fxBank.attrib['id']

        toReturn[id] = {}
        toReturn[id]['models'] = {}
        models = toReturn[id]['models']

        for modelXml in fxBank.iter('Model'):

            name = modelXml.attrib['name']
            id = modelXml.attrib['id']

            models[name] = {}
            model = models[name]

            model['name'] = name
            model['id'] = id

            model['settings'] = {}
            settings = model['settings']

            for settingXml in modelXml.iter('Setting'):
                outerId = settingXml.attrib['outer_id']
                id = settingXml.attrib['id']

                settings[(int(outerId), int(id))] = {}
                setting = settings[(int(outerId), int(id))]

                for name, value in settingXml.attrib.items():
                    setting[name] = value

    return toReturn


    