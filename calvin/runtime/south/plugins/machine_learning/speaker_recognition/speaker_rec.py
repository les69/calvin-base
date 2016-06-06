import subprocess
from subprocess import PIPE
import os
import json
jar_path = "{0}/calvin/runtime/south/plugins/machine_learning/speaker_recognition/{1}".format(os.getcwd(),'recognito.jar')

def add_model(model_name, wav_file):
    pass

def verify_model(model_name, wav_file, frequency=None):

    if frequency is None:
        proc = subprocess.Popen(["java","-jar",jar_path,"identifyModel",wav_file,model_name],  stdin=PIPE, stdout=PIPE)
    else:
        proc = subprocess.Popen(["java","-jar",jar_path,"identifyModel",wav_file,model_name, frequency],  stdin=PIPE, stdout=PIPE)

    (stdin,stderr) = proc.communicate()
    return json.loads(stdin)


