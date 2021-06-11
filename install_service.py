import shutil
from shutil import copyfile
import os
import getpass

import sys

import json

import requests
import sys 
  
# total arguments 
n_count = len(sys.argv) 

from datetime import datetime
import os.path

try:
    app_path = os.path.dirname(os.path.realpath(__file__))
except:
    app_path = "/home/jetson/chooch_ai_service"
    

def get_model_device_info(device_id):
    
    url = "https://api.chooch.ai/predict/device_info/?device_id={}".format(device_id)

    response = requests.post(url, verify=False)

    model_data = json.loads(response.content)
    
    return model_data


def replace_value(input_file, output_file, find_string_val, replace_string_val):
    
    #input file
    fin = open(input_file, "rt")
    #output file to write the result to
    fout = open(output_file, "wt")
    #for each line in the input file
    for line in fin:
         #read replace the string and write to output file
         fout.write(line.replace(find_string_val, replace_string_val))
    #close input and output files
    
    
    fin.close()
    fout.close()
    
    
    
def replace_value_2(input_file, output_file, find_string_val, replace_string_val, find_string_val_2, replace_string_val_2):
    
    #input file
    fin = open(input_file, "rt")
    #output file to write the result to
    fout = open(output_file, "wt")
    #for each line in the input file
    for line in fin:
         #read replace the string and write to output file
         fout.write(line.replace(find_string_val, replace_string_val).replace(find_string_val_2, replace_string_val_2))
      
    #close input and output files
    
    

    fin.close()
    fout.close()    
    
def replace_value_3(input_file, output_file, find_string_val, replace_string_val, find_string_val_2, replace_string_val_2, find_string_val_3, replace_string_val_3):
    
    #input file
    fin = open(input_file, "rt")
    #output file to write the result to
    fout = open(output_file, "wt")
    #for each line in the input file
    for line in fin:
         #read replace the string and write to output file
         fout.write(line.replace(find_string_val, replace_string_val).replace(find_string_val_2, replace_string_val_2).replace(find_string_val_3, replace_string_val_3))
      
    #close input and output files
    
    

    fin.close()
    fout.close()    
    
def replace_value_4(input_file, output_file, replacement_list):
    
    #input file
    with open(input_file) as infile, open(output_file, 'w') as outfile:
        for line in infile:
            for item in replacement_list:
                line = line.replace(item["key_id"], item["key_val"])
            outfile.write(line)
        
        
    
    
app_path = os.path.dirname(os.path.realpath(__file__))



# write device_id


if n_count == 1:    
      device_id = input("Please enter device_id: ")        
else: 
      device_id = str(sys.argv[1]).strip()
        
        
        
model_data = get_model_device_info(device_id)  

print(model_data)

now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")

data_new_info = {}
data_new_info["device_id"] = device_id

try:

    data_new_info["last_update"] = str(date_time)
    data_new_info["models"] = model_data["models"]
    data_new_info["camera_feeds"] = model_data["cameras"]     
    data_new_info["device_info"] = model_data["device_info"]    
except:
    print("Invalid device_id !")
    sys.exit()

with open("{}/data/config.json".format(app_path), 'w', encoding='utf-8') as f:
              json.dump(data_new_info, f, ensure_ascii=False, indent=4)   



# replace values

user_name = getpass.getuser()

# create parameters

replacement_list = []

# run command

device_platform = str(model_data["device_info"]["device_platform"]).strip()
#device_platform == "pc_redhat7_gpu"

if device_platform == "jetson":
    
    key_val = "--runtime nvidia"
    
elif device_platform == "pc_cpu_intel":
    
    key_val = ""
    
elif device_platform == "pc_redhat7_gpu":
    
    key_val = "-e NVIDIA_VISIBLE_DEVICES=all"
    
else:
    
    key_val = "--gpus all"
    

replacement_item = {}
replacement_item["key_id"] = "{run_command}"
replacement_item["key_val"] = key_val
replacement_list.append(replacement_item)

#logs

if device_platform == "jetson":
    
    key_val = "--log-opt max-size=50m"
    
elif device_platform == "pc_cpu_intel":
    
    key_val = "--log-opt max-size=50m"

elif device_platform == "pc_redhat7_gpu":
    
    key_val = ""
    
else:
    
    key_val = "--log-opt max-size=50m"
    
replacement_item = {}
replacement_item["key_id"] = "{logs}"
replacement_item["key_val"] = key_val
replacement_list.append(replacement_item)


replacement_item = {}
replacement_item["key_id"] = "{data_path}"
replacement_item["key_val"] =app_path + "/data"
replacement_list.append(replacement_item)


replacement_item = {}
replacement_item["key_id"] = "{user_name}"
replacement_item["key_val"] = user_name
replacement_list.append(replacement_item)


replacement_item = {}
replacement_item["key_id"] = "{docker_name}"
replacement_item["key_val"] = str(data_new_info["device_info"]["device_docker"])


    
replacement_list.append(replacement_item)



#replace_value_3("{}/install/chooch_predict_on_prem_base.service".format(app_path),  "{}/chooch_predict_on_prem.service".format(app_path),   "{data_path}", app_path + "/data", "{user_name}", user_name, "{docker_name}", data_new_info["device_info"]["device_docker"])


# get user name



#replace_value_2("{}/chooch_predict_on_prem.service".format(app_path),  "{}/chooch_predict_on_prem.service".format(app_path),   "{user_name}", user_name)



replace_value_4("{}/install/chooch_predict_on_prem_base.service".format(app_path),  "{}/chooch_predict_on_prem.service".format(app_path), replacement_list)


    
replace_value("{}/install/chooch_run_base.sh".format(app_path),  "chooch_run.sh",   "{app_path}", app_path) 



file_1 = open("{}/data/processor_platform.txt".format(app_path), "w")
    
if device_platform == "pc_cpu_intel":
    
    file_1.write("cpu_intel")
    
else:
    
    file_1.write("gpu")


# give docker right

os.system("sudo groupadd docker")

os.system("sudo usermod -aG docker $USER")


os.system("sudo chmod 666 /var/run/docker.sock")


# pull docker


latest_docker_image = data_new_info["device_info"]["device_docker"]

    
os.system("sudo docker pull {}".format(latest_docker_image))


# give excute rights to choochrun.sh
os.system("sudo chmod +x chooch_run.sh")

# copy database
os.system("sudo cp chooch_predict_on_prem.service /etc/systemd/system")


#copy service file
if os.path.isfile("data/database/chooch_database.db") == False:
    
    if os.path.exists("data/database") == False:    
         os.mkdir("data/database") 
            
    os.system("sudo cp install/chooch_database.db data/database")


#Give rights to service
os.system("sudo systemctl enable chooch_predict_on_prem.service")
os.system("sudo systemctl daemon-reload")

if device_platform != "pc_redhat7_gpu":

    os.system("sudo systemctl stop apt-daily.timer")
    os.system("sudo systemctl stop apt-daily.service")
    os.system("sudo systemctl disable apt-daily.timer")
    os.system("sudo systemctl disable apt-daily.service")


# Start service
os.system("sudo systemctl start chooch_predict_on_prem.service")

#copyfile("choochtrain.service",  "/etc/systemd/system/choochtrain.service")

