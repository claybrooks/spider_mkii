
'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
class Knob(object):

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __init__(self, id, name, initialValue = 0):
        self._name  = name
        self._id    = id
        self._value = initialValue

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __str__(self):
        return f'{self._name}: {self._value}'

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def getValue(self):
        return self._value

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def setValue(self, newValue):
        self._value = newValue