import sys
import os
import json

from controller import process_video

string = process_video(sys.argv[1])
base = os.path.basename(sys.argv[1])
name = os.path.splitext(base)[0]
jsonarray = json.loads(string)
with open("output/" + name + "output.txt","a", encoding="ISO-8859-1") as output:
    for element in jsonarray:
        output.write("Word: {} , SpeakerTag: {} ".format(element["word"], element["speaker tag"]))
        output.write("\n")
