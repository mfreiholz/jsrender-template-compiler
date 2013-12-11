#!/usr/bin/python
# -*- coding: utf-8

import argparse
import os
import re
import string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", required = True, help = "Base directory in which the script will search for *.tmpl files.")
    parser.add_argument("-o", "--outputfile", required = True, help = "Path to the output file.")
    parser.add_argument("--trim", dest = "trim", action = "store_true")
    parser.add_argument("--newline", dest = "newline", action = "store_true")
    args = parser.parse_args()

    if not args.directory or not args.outputfile:
        return None

    # Create output file.
    outputFile = None
    try:
        outputFile = open(args.outputfile, "w+")
    except IOError:
        print "Oops!"
        return None
    
    # Iterate all available template files and write it's contents into the output file.
    for parentPath, fileName in walkGen(args.directory):
        path = os.path.join(parentPath, fileName)
        try:
            print "Read template => %s" % path
            f = open(path)
            for lineData in f:
                lineBreak = False
                if args.newline and re.search("</script>", lineData, re.IGNORECASE):
                    lineBreak = True
                if args.trim:
                    lineData = lineData.strip("\n\r\t ")
                outputFile.write(lineData)
                if lineBreak:
                    outputFile.write("\n")
            f.close()
        except IOError:
            print "Can not open template file => %s" % path
            
    # Cleanup
    outputFile.close()
        

def walkGen(baseDirectoryPath, fileMatchExpression = "\.tmpl$"):
    """Generator for all template files.
    Walks through the entire baseDirectoryPath and yields for each
    found template file. The fileMatchExpresseion is a regular expression
    pattern to match the file names.
    """
    for parentPath, dirnames, fileNames in os.walk(baseDirectoryPath):
        for fileName in fileNames:
            if re.search(fileMatchExpression, fileName, re.IGNORECASE):
                yield parentPath, fileName


def format(data):
    pass

if __name__ == "__main__":
    main()
