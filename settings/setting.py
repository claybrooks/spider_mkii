
'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
class Setting(object):

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __init__(self, config_data):

        self._outer_id  = config_data['outer_id']
        self._id        = config_data['id']
        self._name      = config_data['name']
        self._type      = config_data['type']

        self._rawValue  = None
        
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def validateValue(self, newValue):
        raise NotImplementedError("Please Implement Validate")

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def setValue(self, newValue):
        if not self.validateValue(newValue):
            return False
        
        self._rawValue = newValue
        return True