'''
lpgen - module to generate PTM light position files

should do:
    - given base LP file, list of filenames and output LP file should be able to generate another LP file based on this  

Created on 15 Mar 2011

@author: Michael Hodgson
'''

def generateLPFile(baseLpFilepath, imagePaths, outputLpFilepath, seperator="\t"):
    lpin = open(baseLpFilepath, "r")
    # first line of the lp file should contain the number of light positions
    noLightsIn = int(lpin.readline())
    if len(imagePaths) != noLightsIn:
        lpin.close()
        raise Exception("The number of light positions in the input file does not match the number of supplied filenames.")
    outlines = []
    for imgPath in imagePaths:
        line = lpin.readline()
        # example line of light position file ../Samplexx/xx-001.tga    -0.015760 0.196076 0.980462
        (linebefore, linesep, lineafter) = line.partition(seperator)
        # the part we want is lineafter
        print linebefore
        print linesep
        print lineafter # just to check
        outlines.append(imgPath + seperator + lineafter.strip("\n"))
    lpin.close()
    print outlines
    lpout = open(outputLpFilepath, "w")
    lpout.write(str(len(outlines)) + "\n")
    for outline in outlines:
        lpout.write(outline + "\n")
    lpout.close()