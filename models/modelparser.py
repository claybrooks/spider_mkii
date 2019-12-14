import lxml.etree as et
import copy

'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
def parseXml(xmlFilePath):

    try:
        with open(xmlFilePath, 'r') as f:
            modelBanksXml = et.parse(f).getroot()
    except Exception as e:
        print (e)
        return

    # the data to return
    toReturn = {}

    # get the id for the model banks message
    toReturn['id'] = int(modelBanksXml.attrib['id'])

    # container for the model banks
    toReturn['modelBanks'] = {}
    modelBanks = toReturn['modelBanks']

    parseModelBanks(modelBanksXml, modelBanks)

    return toReturn

'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
def parseModelBanks(xml, modelBanks):

    for modelBankXml in xml.iter('ModelBank'):

        # get the id for this model bank
        id = int(modelBankXml.attrib['id'])

        modelBanks[id] = {}
        modelBanks[id]['id'] = id

        modelBanks[id]['settings'] = {}
        settings = modelBanks[id]['settings']

        modelBanks[id]['models'] = {}
        models = modelBanks[id]['models']

        parseSettings(modelBankXml.find('Settings'), settings)
        parseModels(modelBankXml.find('Models'), models)

'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
def parseSettings(xml, settings):
    for settingXml in xml.iter('Setting'):  
        outerId = settingXml.attrib['outer_id']
        id      = int(settingXml.attrib['id'])
        type    = settingXml.attrib['type']

        settings[(int(outerId), int(id))] = copy.deepcopy(settingXml.attrib)

        if type == 'multi':
            settings[(int(outerId), int(id))]['values'] = {}

            for value in settingXml.iter('Value'):
                settings[(int(outerId), int(id))]['values'][value.attrib['id']] = copy.deepcopy(value.attrib)
            
'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
def parseModels(xml, models):

    for modelXml in xml.iter('Model'):

        name = modelXml.attrib['name']
        id = int(modelXml.attrib['id'])

        models[id] = {}
        model = models[id]

        model['name'] = name
        model['id'] = id

        model['settings'] = {}
        settings = model['settings']
 
        parseSettings(modelXml.find('Settings'), settings)