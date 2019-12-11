
import usb

import knobs.knobparser     as knobparser
import knobs.knobbank       as knobbank

import models.modelparser   as modelparser
import models.modelbank     as modelbank

'''
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
'''
class SpiderMKii(object):

    # TODO Put all this in a configuration file

    # TODO Figure these out
    get_selected_prepend    = [0x04, 0xf0, 0x00, 0x01, 0x04, 0x0c, 0x12, 0x07, 0x04, 0x7c, 0x00, 0x00, 0x07, 0x00]
    get_selected_append     = [0xf7]

    # TODO Figure these out
    preset_prefix           = 60#192

    # For the three knobs that have three different modes each
    effect_mode_prefix  = 54
    MODE_OFF            = 0
    MODE_GAIN           = 1
    MODE_AUTO           = 3
    MODE_PITCH          = 5
    MODE_CHORUS         = 7
    MODE_PHASER         = 9
    MODE_TREMOLO        = 11
    MODE_DELAY          = 13
    MODE_TAPE_ECHO      = 15
    MODE_SWEEP_ECHO     = 17

    effect_mode = {
        MODE_OFF:           'OFF',
        MODE_GAIN:          'GAIN',
        MODE_AUTO:          'AUTO',
        MODE_PITCH:         'PITCH',
        MODE_CHORUS:        'CHORUS',
        MODE_PHASER:        'PHASER',
        MODE_TREMOLO:       'TREMOLO',
        MODE_DELAY:         'DELAY',
        MODE_TAPE_ECHO:     'TAPE_ECHO',
        MODE_SWEEP_ECHO:    'SWEEP_ECHO',
    }

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __init__(self, vendorId, productId):
        
        self._isConnected = False
        
        self._vendorId  = vendorId
        self._productId = productId
        
        self._dev       = None
        self._cfg       = None
        self._intf      = None
        self._ep_in     = None
        self._ep_out    = None

        self._curr_gain_auto_pitch_mode         = 0
        self._curr_chorus_phaser_tremolo_mode   = 0
        self._curr_delay_tape_sweep_mode        = 0

        self._curr_preset_id                    = 0

        # datastore
        #self._knobBank = knobbank.KnobBank('spider_mkii_knobs.xml')

        # create our knobs
        #for id, name in SpiderMKii.knobs.items():
        #    self._knobs[id] = knob.Knob(id, name, 0)

        self._modelBanks = {}

        configData = modelparser.parseXml('models/spider_mkii_model.xml')
        for id, config in configData.items():
            self._modelBanks[id] = modelbank.ModelBank(config['models'])

        configData = knobparser.parseXml('knobs/spider_mkii_knobs.xml')
        self._knobBank = knobbank.KnobBank(configData)

        self.connect()

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def getSelectionBuffer(self, choice):
        return SpiderMKii.get_selected_prepend + [choice] + SpiderMKii.get_selected_append

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def connect(self):

        # try to connect
        self._dev = usb.core.find(idVendor=self._vendorId, idProduct=self._productId)

        # say we connected or not
        if not self._dev:
            return False

        self._dev.set_configuration()

        # get an endpoint instance
        self._cfg = self._dev.get_active_configuration()

        self._intf =  self._cfg[(1,0)]

        self._ep_in = usb.util.find_descriptor(
            self._intf,
            custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )

        self._ep_out = usb.util.find_descriptor(
            self._intf,
            custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )

        self._isConnected = True

        return True

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __handleKnobs(self, data):

        id  = data[2]
        val = data[3]

        if id not in self._knobs.keys():
            print (f'Unknown Knob ID: {id}')
            print (data)
            return

        self._knobs[id].setValue(val)

        ''' if id == 27:
            print (f'{effect_mode[curr_gain_auto_pitch_mode]}: {val}')
        elif id == 96:
            print (f'{effect_mode[curr_chorus_phaser_tremolo_mode]}: {val}')
        elif id == 30:
            print (f'{effect_mode[curr_delay_tape_sweep_mode]}: {val}')
        else:'''

        print (self._knobs[id])

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __handleEffectMode(self, data):
        
        mode_val = data[1]

        if mode_val == 0:
            self._curr_delay_tape_sweep_mode        = 0
            self._curr_chorus_phaser_tremolo_mode   = 0
            self._curr_gain_auto_pitch_mode         = 0
        elif mode_val <= 5:
            self._curr_gain_auto_pitch_mode         = mode_val
        elif mode_val <= 11:
            self._curr_chorus_phaser_tremolo_mode   = mode_val
        elif mode_val <= 17:
            self._curr_delay_tape_sweep_mode        = mode_val

        print (data)

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __handleChorusPhaserTremolo(self, data):
        if self._curr_gain_auto_pitch_mode != data[1]:
            self._curr_gain_auto_pitch_mode = data[1]
            print (f'CHORUS_PHASER_TREMOLO MODE: {SpiderMKii.effect_mode[self._curr_chorus_phaser_tremolo_mode]}')
    
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __handlePreset(self, data):
        self._curr_preset_id = data[2]
        print (f'Preset: {self._curr_preset_id}')

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def handleIncomingData(self, data):

        if data == None or len(data) == 0:
            return None

        id = data[0]

        if id == SpiderMKii.knob_prefix:
            self.__handleKnobs(data)
        elif id == SpiderMKii.effect_mode_prefix:
            self.__handleEffectMode(data)
        elif id == SpiderMKii.preset_prefix:
            self.__handlePreset(data)
        else:
            print (data)

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def getSelection(self, choice):

        if not self.isReadable() or not self.isWriteable():
            return None

        # get status of something
        self.__write(self.getSelectionBuffer(choice))

        shouldRead = True
        toReturn = []

        # read until we fail
        while shouldRead:
            # get read flag and data
            shouldRead, data = self.__read()

            # if we got data, append to our return list
            if shouldRead:
                toReturn.append(data)

        # say whether or not we got data, and return none if we didn't
        return toReturn
 
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def isReadable(self):
        return self.__isValid(self._ep_in)
 
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def isWriteable(self):
        return self.__isValid(self._ep_out)
 
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __isValid(self, ep):
        return (self._isConnected) and (self._dev != None) and (ep != None)

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __read(self):
        # helper return value
        bad_read = (False, None)
        
        try:
            return (True, self._dev.read(self._ep_in.bEndpointAddress, self._ep_in.wMaxPacketSize))
        except Exception:
            return bad_read

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def read(self):
        if not self.isReadable():
            return False, None

        return self.__read()
            
    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def __write(self, data):

        try:
            self._dev.write(self._ep_out.bEndpointAddress, data)
            return True
        except Exception:
            return False

    '''
    ####################################################################################################################
    #                                                                                                                  #
    ####################################################################################################################
    '''
    def write(self, data):

        if not self.isWriteable():
            return False

        return self.__write(data)