from .LoopPedal import LoopPedal


def create_instance(c_instance):
    ''' Creates and returns Remote Script instance '''
    return LoopPedal(c_instance)
