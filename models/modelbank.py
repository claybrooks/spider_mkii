import models.model as model
import settings.typemap as typeMap
'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
class ModelBank(object):

    currentModelId = 0

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __init__(self, config_data):
        self._id = config_data['id']
        self._models = {}
        self._settings = {}

        for id, settingConfig in config_data['settings'].items():
            self._settings[id] = typeMap.typeMap[settingConfig['type']](settingConfig)

        for id, modelConfig in config_data['models'].items():
            self._models[id] = model.Model(modelConfig)
    
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def getId(self):
        return self._id
    
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def setModelData(self, id, settingId, data):
        if id not in self._models.keys():
            print (f'Unknown Model Id: {id}')

        self._models[id].setSettingValue(settingId, data)
    
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def setSettingData(self, settingId, data):
        if id not in self._settings.keys():
            print (f'Unknown Setting Id: {id} in Model: {self._id}')

        self._settings[id].setValue(settingId, data)
        
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def getModel(self, id):
        if id not in self._models.keys():
            return None

        return self._models[id]
        
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def getSelectedModel(self):
        id = (self._id, ModelBank.currentModelId)
        if id not in self._settings:
            return None
        return self._settings[id].getRawValue()
       
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def handleData(self, data):
        # This is the combo of the model bank and settings within model bank.  It'll either be id or id*2.  look at the
        # xml
        id          = (data[11], data[13])
        if (data[14] == 64) and (data[15] == 0):
            value = -1 * (data[15] << 7) | (data[17])
        else:
            value = (data[14] << 14) | (data[15] << 7) | (data[17])

        handled = False

        # we are directly changing a setting of the model bank
        if id in self._settings.keys():
            self._settings[id].setValue(value)
            print (self._settings[id])
            handled = True
        else:
            modelId = self.getSelectedModel()
            
            if modelId in self._models.keys():
                self._models[modelId].setSettingValue(id, value)
                print(self._models[modelId].getSetting(id))
                handled = True

        if not handled:
            print (data)