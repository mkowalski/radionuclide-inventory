from fma import FMA
from scanner import scanner


def FindRadionuclideInventory ():
    originalInventory = []
    scanner('Andra_FMA', originalInventory, '#')


    # fake inventory
    finv = [["H-3", float(9.84812486279e-06)],
            ["Al-26", float(7.55041470047e-12)],
            ["Ni-63", float(1.20418139837e-08)]]

    FMA(finv)

    return ()
