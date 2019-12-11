import lxml.etree as et
import copy

def parseXml(xmlFilePath):

    try:
        with open(xmlFilePath, 'r') as f:
            knobs = et.parse(f).getroot()
    except Exception as e:
        print (e)
        return

    toReturn = {}

    for knob in knobs.iter('Knob'):
        toReturn[int(knob.attrib['id'])] = copy.deepcopy(knob.attrib)

    return toReturn