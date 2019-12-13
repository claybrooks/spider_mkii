import lxml.etree as et
import copy

def parseXml(xmlFilePath):

    try:
        with open(xmlFilePath, 'r') as f:
            knobs = et.parse(f).getroot()
    except Exception as e:
        print (e)
        return

    id = int(knobs.attrib['id'])

    toReturn = {}

    toReturn['knobs'] = {}

    toReturn['id'] = id
    for knob in knobs.iter('Knob'):
        toReturn['knobs'][int(knob.attrib['id'])] = copy.deepcopy(knob.attrib)

    return toReturn