import model

'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
class EffectBank(object):

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __init__(self, models):

        self._models = {}
        for id, modelConfig in models.items():
            self._models[id] = model.Model(modelConfig)

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def getModel(self, id):
        if id not in self._models.keys():
            return None

        return self._models[id]