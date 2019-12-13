import settings.typemap         as typeMap
import settings.binarysetting   as binarysetting
import settings.analogsetting   as analogsetting
import settings.multisetting    as multisetting

'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
class Model(object):

    # SETTINGS SELECTION
    SETTINGS_FX_1   = [[52, 99, 0, 16], [52, 99, 0, 32]]
    SETTINGS_FX_2   = [[52, 99, 0, 17], [52, 99, 0, 33]]
    SETTINGS_FX_3   = [[52, 99, 0, 18], [52, 99, 0, 2], [52, 99, 0, 34]]
    SETTINGS_REVERB = [[52, 99, 0, 19], [52, 99, 0, 35]]

    SETTINGS_FX_1= [52, 99, 0, 16]
    SETTINGS_VOL = [52, 99, 0, 2]
    SETTINGS_LOOP = [52, 99, 0, 4]

    # REVERB MODEL
    MODEL_REVERB_LUX_SPRING     = 19
    MODEL_REVERB_VINT_PLATE     = 20
    MODEL_REVERB_STD_SPRING     = 57
    MODEL_REVERB_KING_SPRING    = 58
    MODEL_REVERB_SLAP_PALTE     = 66
    MODEL_REVERB_LARGE_PLATE    = 63
    MODEL_REVERB_SMALL_ROOM     = 67
    MODEL_REVERB_TILED_ROOM     = 68
    MODEL_REVERB_BRIGHT_ROOM    = 59
    MODEL_REVERB_CHAMBER        = 60
    MODEL_REVERB_RICH_CHAMBER   = 65
    MODEL_REVERB_MEDIUM_HALL    = 64
    MODEL_REVERB_LARGE_HALL     = 62
    MODEL_REVERB_DARK_HALL      = 61
    MODEL_REVERB_CAVERNOUS      = 69

    # WAH MODEL
    MODEL_WAH_VETTA             = 0
    MODEL_WAH_CHROME            = 1
    MODEL_WAH_COLORFUL          = 2
    MODEL_WAH_WEEPER            = 3
    MODEL_WAH_CONDUCTOR         = 4
    MODEL_WAH_CUSTOM_CHROME     = 5
    MODEL_WAH_FASSEL            = 6
    MODEL_WAH_THROATY           = 7
    

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################\
    '''
    def __init__(self, config_data):
        
        self._name = config_data['name']
        self._id = config_data['id']

        self._settings = {}
        for id, settingConfig in config_data['settings'].items():
            self._settings[id] = typeMap.typeMap[settingConfig['type']](settingConfig)

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################\
    '''
    def getSetting(self, key):
        if key not in self._settings.keys():
            return None

        return self._settings[key]
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################\
    '''
    def setSettingValue(self, key, value):
        if key not in self._settings.keys():
            return False

        return self._settings[key].setValue(value)

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################\
    '''
    def getSettingValue(self, key):
        if key not in self._settings.keys():
            return None
            
        return self._settings[key].getValue()