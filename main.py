#!/usr/bin/env python

import os, numpy
from scanner import oldScanner as scanner
# from tools import AboveDeclarationWhenIras, AboveDeclarationForGivenCurrent
from tool_FMA import AboveDeclarationForGivenCurrent, FMA, \
    BelowMDAForGivenCurrent


# This module verifies if a nuclide is already part of an inventory
# If not: it adds it to the inventory
# If yes: it returns 1.0 value

def AddNuclide(nuclide, inventory):
    found = 'No'
    for a in inventory:
        if a == nuclide:
            found = 'Yes'
    if found == 'No':
        inventory.append(nuclide)
    if found == 'Yes':
        return (1.0)
    else:
        return (0.0)


# This module finds the scaling factor from a given inventory
# It returns the activity of the key nuclide and the corresponding value
# of the scaling factor

def FindScalingFactor(nuclideDMN, keyNuclide, inventory):
    activityKeyNuclide = 0.  # Initialization
    activityDMN = 0.
    # Loop to find key nuclide and DMN
    for a in inventory:
        if a[0] == keyNuclide: activityKeyNuclide = a[1]
        if a[0] == nuclideDMN: activityDMN = a[1]
    if activityKeyNuclide > 0.:
        scalingFactor = activityDMN / activityKeyNuclide
        return (activityKeyNuclide, scalingFactor)
    else:
        return ()


def AnalysisOneMaterial(matName, keyNuclide, DMN, Directory):
    DirectoryResults = Directory + '/' + matName  # Directory with the results from ActiWiz
    DirectorySF = DirectoryResults + '_SF'  # Directory with the scaling factors
    if not os.path.exists(DirectorySF):  # Create the directory if not existing
        os.makedirs(DirectorySF)

    # List of files to be analysed, with Actiwiz results
    ListFiles = os.listdir(DirectoryResults)

    for nuclide in DMN:
        ScalingList = []

        for fileName in ListFiles:

            originalInventory = []
            scanner(DirectoryResults + '/' + fileName, originalInventory, '#')

            try:
                activityKeyNuclide, ScalingFactorDMN = FindScalingFactor(
                    nuclide, keyNuclide, originalInventory, )
                ScalingList.append([activityKeyNuclide, ScalingFactorDMN,
                                    fileName])  # activityKeyNuclide*1.0E10

                ScalingList.sort(lambda x, y: cmp(x[0], y[0]))
            except:
                pass

        # Open the file in the desired directory and save the data
        f = open(DirectorySF + '/' + nuclide + '_' + keyNuclide, 'w')
        # Writing the first line of comment, with the input parameters#
        f.write("# Activity of key nuclide,  Scaling Factor,Scenario\n")
        # Writing the scaling factors, line by line

        for a in ScalingList:
            #            b=[a[1],a[2]] # Artefact to pick up only the last two values and skip a[0], which is the nuclide
            f.write(" ".join(map(lambda x: str(x), a)) + "\n")

    return ()


def FindRadionuclideInventory(matName, SE_FMA, Directory):
    DirectoryResults = Directory + '/' + matName  # Directory with the results from ActiWiz
    DirectoryRN = DirectoryResults + '_RN'  # Directory with the scaling factors
    if not os.path.exists(DirectoryRN):  # Create the directory if not existing
        os.makedirs(DirectoryRN)

    # List of files to be analysed, with Actiwiz results
    ListFiles = os.listdir(DirectoryResults)

    ListNuclidesFMA = []

    # Loop to analyse all the files with the Actiwiz results
    for fileName in ListFiles:
        originalInventory = []
        scanner(DirectoryResults + '/' + fileName, originalInventory, '#')

        # The following list contains nuclides with activity above declaration
        shortInventoryFMA = FMA(SE_FMA, originalInventory)

        # List of nuclides as above, but cumulative over all the scenarios
        for a in shortInventoryFMA:
            AddNuclide(a[0], ListNuclidesFMA)

    # Open the file in the desired directory and save the data
    f = open(DirectoryRN + '/RadionuclideInventory_FMA_' + str(SE_FMA), 'w')
    # Writing the radionuclides
    for a in ListNuclidesFMA:
        f.write("".join(map(lambda x: str(x), a)) + "\n")
    f.close()

    return ()


# print "List of nuclides which can be above decl. limits when IRAS = 1"
# for a in ListNuclidesIRAS:    print a


# def mean_abs_dev(pop):
# n = float(len(pop))
# mean = sum(pop) / n
# diff = [ abs(x - mean) for x in pop ]
# return sum(diff) / n

# Main program for data analysis

# List of difficult to measure nuclides, for which we want to establish a scaling factor!!!
# materials = ['Copper_CuOFE','Steel_304L', 'Aluminium_6060', 'Steel_low_carb']
materials = ["Aluminium_6060"]
keyNuclide = ["Na-22"]  # ["Na-22", "Co-60", "Ti-44", "Fe55"]
# DMN = ["H-3","Zn-65", "Na-22","Fe-55",  "Cl-36", "Sb-125", "Mn-54",  "Co-60","Ag-108m", "Ba-133","C-14", ,"Rh-101","Bi-207", "Hg-194", "Cd-113m","Al-26",
# "Ti-44", "Cs-137", "Be-10",  "Pb-202", "Pt-193", "Gd-148", "Mo-93", "Si-32",  "Ca-41"]

# ["H-3","Ag-110m","Sn-119m","Fe-55", "Co-60", "Sb-125","Zn-65","Co-57","Cl-36","Mn-54","Ag-108m", "Na-22", "Ni-63", "Sn-121m" , "Rh-101", "V-49","Rh-102", "Ti-44","Bi-207", "C-14"  ]
# DMN = ["H-3",	"Ni-63","Cl-36","Co-60", "Sn-121m", "Fe-55", "Ag-108m",	"Sb-125", "Na-22", "Ti-44", "Ba-133", "Rh-101", "Ag-110m", "C-14", "Bi-207", "Mn-54", "Hg-194",	"Zn-65", "Co-57", "Rh-102", "Mo-93", "Ca-41", "Be-10",	"Cs-137", "Sn-119m", "Si-32", "Pb-202"]


# for steel 304L
# DMN=["Fe-55", "Mn-54","H-3","Ni-63","Ni-59","C-14"]
# for copper CuOFE
# DMN=["Fe-55", "Mn-54","H-3","Ni-63","Ni-59","C-14","Zn-65"]
# for aluminium 6060
DMN = ["Fe-55", "Mn-54", "H-3", "Ni-63", "C-14"]
Directory = 'Results'

for matName in materials:
    # FindRadionuclideInventory (matName,37000 , Directory)
    FindRadionuclideInventory(matName, 37000, Directory)

for matName in materials:
    for Nuclide in keyNuclide:
        AnalysisOneMaterial(matName, Nuclide, DMN, Directory)
