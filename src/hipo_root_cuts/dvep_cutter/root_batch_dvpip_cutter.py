import subprocess
import os
import time
import shutil
from shutil import copyfile

#This project
from src.utils import data_getter
from src.utils import query_maker
from src.utils import file_maker



fs = data_getter.get_json_fs()

#datafile_dir = "F18_Inbending_SangbaekSkim_20200129/"
datafile_dir = "testsim_results/"
data_dir = fs['base_dir']+fs['data_dir']+fs["data_2_dir"]+datafile_dir
data_list = os.listdir(data_dir)


#For FD
root_macro_script = "dvpip_cutterFD.C"
data_out_dir = datafile_dir
#For CD
#root_macro_script = "dvpip_cutterCD.C"
#data_out_dir = "datafile_dir"

root_macro = fs['base_dir']+fs['src_dir']+fs['dvep_cut_dir']+root_macro_script

output_dir = fs['base_dir']+fs['data_dir']+fs["data_3_dir"]+data_out_dir
file_maker.make_dir(output_dir)



default_root_outname = "output_root_file.root"
default_root_inname = "input_root_file.root"
for count,file in enumerate(data_list):
    print("on file {} out of {}, named {}".format(count+1,len(data_list),file))
    copyfile(data_dir+file,default_root_inname)
    process = subprocess.Popen(['root','-b','-q', root_macro],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    #print("STDOUT is {}".format(stdout))
    print("STDERR is {}".format(stderr))
    shutil.move(default_root_outname,output_dir+file.replace(".root","_DVEP.root"))
    time.sleep(0.5)

