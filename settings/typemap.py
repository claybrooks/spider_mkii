import settings.binarysetting as binarysetting
import settings.multisetting as multisetting
import settings.analogsetting as analogsetting

typeMap = {
    'binary': binarysetting.BinarySetting,
    'analog': analogsetting.AnalogSetting,
    'multi' : multisetting.MultiSetting,
}
