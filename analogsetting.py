import setting

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
        super.__init__(config_data)

        self._analogMin = config_data['analogMin']
        self._analogMax = config_data['analogMax']
        self._valueType = config_data['valueType']
        self._valueMin  = config_data['valueMin']
        self._valueMax  = config_data['valueMax']

        
        self._adjustedAnalogMin = 0
        self._adjustedAnalogMax = self._analogMax - self._analogMin

        self._adjustedValueMin = 0
        self._adjustedValueMax = self._valueMax - self._valueMin

        self._adjustedMin = 0
        self._adjustedMax = None

        self._adjustedValueMin = 0
        self._adjustedValueMax = None

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def getValue(self):
        percentAnalogApplied = (self._rawValue - self._analogMin) / (self._adjustedMax)

        valueApplied = (self._adjustedValueMax * percentAnalogApplied) + self._adjustedValueMin

        return valueApplied

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def validateValue(self, value):
        return (value >= self._analogMin) or (value <= self._analogMax)
