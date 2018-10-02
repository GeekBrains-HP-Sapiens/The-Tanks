import Utility.pyganim as pyganim

# import pyganim

def anim_object(anim_list, delay=0.1):

    boltanim = []
    
    for anim in anim_list:

        boltanim.append((anim, delay))
        
    anim = pyganim.PygAnimation(boltanim)

    return anim
