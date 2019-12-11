import lxml.etree as et
import copy

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
                id      = settingXml.attrib['id']
                type    = settingXml.attrib['type']

                settings[(int(outerId), int(id))] = copy.deepcopy(settingXml.attrib)

                if type == 'multi':
                    settings[(int(outerId), int(id))]['values'] = {}

                    for value in settingXml.iter('Value'):
                        settings[(int(outerId), int(id))]['values'][value.attrib['id']] = copy.deepcopy(value.attrib)
    return toReturn


    