#!/usr/bin/python
#
import sys, math
from os import listdir
# from Read_spectro import spectrometry
from scanner import oldScanner as scanner
# from Mandra import Andra_fingerprints, nuclide_list_merge_2
from math import floor, log10


def FMA(SE_FMA, inventory):
    limits = []
    scanner('Andra_FMA_2', limits, "#")

    sum_activity = 0.

    inventoryWithFMA = []
    for a in inventory:
        for b in limits:
            if a[0] == b[0]:
                name = a[0]
                activity = a[1]
                # energy=a[2]
                limit = b[1]
                declaration = b[2]
                maxlimit = b[3]
                emission = b[4]
                FMA_fraction3 = (emission == 1)

                inventoryWithFMA.append([name, activity, FMA_fraction3, declaration, maxlimit, limit])

                sum_activity = sum_activity + activity

            # print (sum_activity)

    RN_list = []

    for c in inventoryWithFMA:
        if c[4] > c[1] / sum_activity * SE_FMA > c[3]:
            RN_list.append([c[0], c[1] / sum_activity * SE_FMA])

    RN_list.sort(lambda x, y: cmp(y[1], x[1]))
    RN_list.sort(key=lambda x: x[0])

    f = open("Results/Aluminium_6060_RA/RadionuclideInventory_RA_", 'a+')

    # f.write(",".join(map(lambda x: str(x), RN_list))+"\n")
    f.write(",".join([','.join(map(str, item)) for item in RN_list]) + "\n")
    # f.write("#"+"".join(RN_list)+"\n")
    f.close()
    print(RN_list)

    return (RN_list)


def ValueORAP(inventory):
    limits = []
    scanner('ORAP', limits, "#")

    totalORAP = 0.

    for a in inventory:
        for b in limits:
            if a[0] == b[0]:
                name = a[0]
                activity = a[1]
                limit = b[1]
                totalORAP = totalORAP + activity * 1000 / limit

    return (totalORAP)


def ValueORAP(inventory):
    limits = []
    scanner('ORAP', limits, "#")

    totalORAP = 0.

    for a in inventory:
        for b in limits:
            if a[0] == b[0]:
                name = a[0]
                activity = a[1]
                limit = b[1]
                totalORAP = totalORAP + activity * 1000 / limit

    return (totalORAP)


def ValueNewORAP(inventory):
    limits = []
    scanner('NewORAP', limits, "#")

    totalORAP = 0.

    for a in inventory:
        for b in limits:
            if a[0] == b[0]:
                name = a[0]
                activity = a[1]
                limit = b[6]
                totalORAP = totalORAP + activity / limit

    return (totalORAP)


def ValueIRAS(inventory):
    limits = []
    scanner('Andra', limits, "#")

    totalIRAS = 0.

    for a in inventory:
        for b in limits:
            if a[0] == b[0]:
                name = a[0]
                activity = a[1]
                limit = b[1]
                totalIRAS = totalIRAS + activity / limit

    return (totalIRAS)


def AboveDeclarationForGivenCurrent(inventory, current):
    limits = []
    scanner('Andra_FMA', limits, "#")

    inventoryAboveDeclaration = []
    for a in inventory:
        for b in limits:
            if a[0] == b[0]:
                name = a[0]
                activity = a[1] * current
                declaration = b[2]
                if activity >= declaration:
                    inventoryAboveDeclaration.append([name, activity])
    inventoryAboveDeclaration.sort(lambda x, y: cmp(y[1], x[1]))

    return (inventoryAboveDeclaration)


def BelowMDAForGivenCurrent(inventory, current):
    limits = []
    scanner('Andra_FMA', limits, "#")

    inventoryBelowMDA = []
    for a in inventory:
        for b in limits:
            if a[0] == b[0]:
                name = a[0]
                activity = a[1] * current
                maxlimit = b[3]
                if activity <= maxlimit:
                    inventoryBelowMDA.append([name, activity])
    inventoryBelowMDA.sort(lambda x, y: cmp(y[1], x[1]))

    return (inventoryBelowMDA)


def round_to_2(x):
    return round(x, -int(floor(log10(x))) + 1)


# Routine to calculate the figure of merit for one set
def evaluate_fingerprints(inventory, limits):
    evaluation = 0.  # Figure of merit
    total_activity = 0.
    ratio = 0.0  # Total fraction of the limit
    activity = 1.  # Default value in case of void list
    for a in inventory:
        activity = a[1]
        total_activity = total_activity + activity
        limit = 0.
        # Find the limit corresponding to the nuclide a[0]
        for b in limits:
            if a[0] == b[0]:
                limit = b[1]
                # Calculate the total fraction of limit
                ratio = ratio + activity / limit

    if total_activity != 0.:
        evaluation = ratio / total_activity
    return evaluation


# Routine to calculate the figure of merit for one set
def evaluate_fingerprints_tracer(inventory, limits, tracer):
    activity_tracer = 0.
    for a0 in inventory:
        if a0[0] == tracer:
            activity_tracer = a0[1]
    if activity_tracer == 0.:
        return activity_tracer

    evaluation = 0.  # Figure of merit
    ratio = 0.0  # Total fraction of the limit
    for a in inventory:
        activity = a[1]
        limit = 0.
        # Find the limit corresponding to the nuclide a[0]
        for b in limits:
            if a[0] == b[0]:
                limit = b[1]
                # Calculate the total fraction of limit
                ratio = ratio + activity / limit

    evaluation = ratio / activity_tracer
    return evaluation


# Routine to select those that contribute > min percentage
def cut_fingerprints(inventory, limits, percentage):
    temp = []
    total_fraction = 0.
    for a in inventory:
        for b in limits:
            if a[0] == b[0]:
                total_fraction = total_fraction + a[1] / b[1]

    for c in inventory:
        for d in limits:
            if c[0] == d[0]:
                if c[1] / d[1] > total_fraction * percentage / 100.:
                    temp.append([c[0], c[1]])

    temp.sort(lambda x, y: cmp(y[1], x[1]))

    return temp


# Routine to read files from Actiwiz (table only)
def read_wiz(file, inventory):
    temp1 = []
    temp2 = []
    total = 0.
    scanner(file, temp1, '#')
    for a in temp1:
        # a[0] is the element name
        # a[2] is the mass number
        # a[3] is the relative activity
        # a[7] is the fraction of LE limit
        temp2.append([a[0] + '-' + str(int(a[2])), a[7]])
        total = total + a[7]
    for b in temp2:
        # b[0] is the nuclide name
        # b[1]/total is the fraction of LE (normalized to 1)
        inventory.append([b[0], b[1] / total])

    return
