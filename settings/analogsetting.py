import settings.setting as setting

'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
class AnalogSetting(setting.Setting):
    
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __init__(self, config_data):
        super().__init__(config_data)

        self._analogMin = float(int(config_data['analogMin'], 16))
        self._analogMax = float(int(config_data['analogMax'], 16))
        self._valueType = config_data['valueType']
        self._valueMin  = float(config_data['valueMin'])
        self._valueMax  = float(config_data['valueMax'])

        
        self._adjustedAnalogMin = 0
        self._adjustedAnalogMax = self._analogMax - self._analogMin

        self._adjustedValueMin = 0 
        self._adjustedValueMax = self._valueMax - self._valueMin

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def getValue(self):
        percentAnalogApplied = (self._rawValue - self._analogMin) / (self._adjustedAnalogMax)

        valueApplied = (self._adjustedValueMax * percentAnalogApplied) + self._valueMin

        return valueApplied

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def validateValue(self, value):
        return (value >= self._analogMin) or (value <= self._analogMax)
