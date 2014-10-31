#!/usr/bin/python
# -*- coding: utf-8

import argparse
import os
import re
import string
import sys

gFilePathExcludeSet = set()

def main():
    parser = argparse.ArgumentParser()
    # Basic input/output file options
    parser.add_argument("-o", "--outputfile", required = True, help = "Path to the minified output file.")
    parser.add_argument("-d", "--directory", required = False, help = "Base directory in which the script will search for *.tmpl files.")
    parser.add_argument("-p", "--directory-file-pattern", dest = "directoryFilePattern", default = "\.tmpl$", help = "File name pattern regex to identify template files for --directory option.")
    parser.add_argument("-t", "--file", action = "append", help = "Path to an template file. This option may be used more than once to add multiple files.")
    # Minifying options
    parser.add_argument("--trim", dest = "trim", action = "store_true", help = "Removes all leading/trailing spaces, tabs and line breaks.")
    parser.add_argument("--newline", dest = "newline", action = "store_true", help = "Inserts a line break after each ending script-tag. Using this option with --trim, will result in a one-template-per-line minified file.")
    args = parser.parse_args()

    if not (args.directory or args.file) or not args.outputfile:
        return None

    # Create output file.
    outputFile = None
    try:
        outputFile = open(args.outputfile, "w+")
    except IOError as e:
        sys.stderr.write("Can not open output file (%d %s) => %s\n" % (e.errno, e.errmsg, args.outputfile))
        return None
    gFilePathExcludeSet.add(os.path.abspath(args.outputfile))
    
    # Iterate all available template files and write it's contents into the output file.
    tmplFileSizeSum = 0.0
    for parentPath, fileName in walkGen(args.directory, args.directoryFilePattern, args.file):
        path = os.path.join(parentPath, fileName)
        if os.path.abspath(path) in gFilePathExcludeSet:
            continue
        try:
            print ("Processing template => %s" % (path))
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
            tmplFileSizeSum += f.tell()
            f.close()
        except IOError as e:
            sys.stderr.write("Can not open template file (%d %s) => %s\n" % (e.errno, e.errmsg, path))
            
    # Cleanup
    outputFile.close()
    
    # Print statistics.
    outputFileSize = float(os.stat(args.outputfile).st_size)
    savesInPerCent = (100 / tmplFileSizeSum) * outputFileSize
    print ("Minified templates from %d bytes to %d bytes (%d%% of the original templates)." % (tmplFileSizeSum, outputFileSize, savesInPerCent))


def walkGen(baseDirectoryPath, fileMatchExpression, fileList):
    """Generator for all template files.
    
    Walks through the entire 'baseDirectoryPath' and yields for each file which
    matches the 'fileMatchExpression'.
    """
    if fileList:
        for f in fileList:
            if os.path.isabs(f):
                yield os.path.split(f)
            else:
                yield os.path.split(os.path.abspath(f))
    
    if baseDirectoryPath:
        for parentPath, dirnames, fileNames in os.walk(baseDirectoryPath):
            for fileName in fileNames:
                if re.search(fileMatchExpression, fileName, re.IGNORECASE):
                    yield parentPath, fileName


if __name__ == "__main__":
    main()