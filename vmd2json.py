import sys
import json
from Log import Log
from Parsers.VMDReader import VMDReader


if len(sys.argv) != 3:
    print("Usage: python vmd2json.py <vmd-file> <output-file>")
    exit(1)
else:
    Log.log("info", "Starting conversion...")
    vmdFile = sys.argv[1]
    outputFile = sys.argv[2]
    vmdReader = VMDReader(vmdFile)
    Log.log("info", "Writing to file: " + outputFile)
    with open(outputFile, "w", encoding = "utf-8") as f:
        json.dump(vmdReader.read(), f, ensure_ascii = False, indent = 4)
    Log.log("info", "Conversion finished.")
