import argparse
import glob
import sys

#Configure command line arguments
parser = argparse.ArgumentParser(
    description='Generate configuration files for CMS Higgs-to-four-leptons Level 4 example.')
parser.add_argument('-n', type=int, default=50,
    help='Number of files to be analyzed witin each configuration file / job. Default is 50')
parser.add_argument('-d','--dataset', type=str,
    help='Specify which dataset you want to analyze. For example: /DoubleMuParked/Run2012B-22Jan2013-v1/AOD')

#Get command line arguments
args = parser.parse_args()
N = args.n                      #Max Number of rootfiles to be input to each newly generated cfg file
input_dataset = args.dataset    #Dataset specified by the user at the command line


#Open file that contains list of sample datasets
with open("code/HiggsExample20112012/Level4/List_indexfile.txt","r") as fi:
    samples = []
    #Read line by line
    for line in fi:
        #Only interested in lines that start with filepath
        if line.startswith('/'):
            #If the user provided a specific dataset at the command line
            if input_dataset is not None:
                #Check to see if that input dataset matches the current line
                if input_dataset in line:
                    line_split1 = line.split('/')[1:-1]
                    line_split2 = line_split1[1].split('-')
                    new_sample = (line_split1[0],line_split2[0])
                    samples.append(new_sample)
            else:
                #Remove the empty first element and the AOD or AODSIM last element
                line_split1 = line.split('/')[1:-1]
                line_split2 = line_split1[1].split('-')
                new_sample = (line_split1[0],line_split2[0])
                samples.append(new_sample)

#Make sure that input dataset was found
if len(samples) == 0:
    sys.exit("ERROR: Input dataset was not found in List_indexfile.txt.")
elif len(samples) == 1:
    print("Generating configuration file(s) for",input_dataset)
else:
    print("Generating configuration files for all datasets in List_indexfile.txt.")


#Get pathnames to all the .txt index files from within the datasets directory
available_index_files = glob.glob('datasets/*.txt', recursive=True)

#Create a dictionary that matches each dataset name to its corresponding index files
dataset_dict = {}
for sample in samples:
    key = sample
    matching_index_files = [fi for fi in available_index_files if all([subkey in fi for subkey in key])]
    dataset_dict[key]=matching_index_files

#Read in the default format for the python configuration files
with open('code/HiggsExample20112012/Level4/default_cfg.py', 'r') as default_cfg:
    default_content = default_cfg.read()


for key,index_files in dataset_dict.items():

    count = 0   #Make a count to keep track the number of cfg files generated for each dataset key
    dataset_id = key[0] + '-' + key[1]
    rootfiles = []

    #Iterate through each of the index files listed within this dataset key
    for index_filename in index_files:
        with open(index_filename,"r") as index_file:

            #Read in the index file and create list of each line without '\n'
            rootfiles.extend( index_file.read().splitlines() )

    #Iterate through each N set of lines
    for i in range(0, len(rootfiles), N):
        #Get new list of N root files
        N_rootfiles = rootfiles[i:i+N]

        #Turn this list of N root files into
        new_input_filenames = '\",\n\"'.join(N_rootfiles)
        new_input_filenames = "[\"" + new_input_filenames
        new_input_filenames = new_input_filenames + "\"]" 

        #Update the count and create the new cfg filename and the new output filename
        count += 1
        new_filename = 'code/HiggsExample20112012/Level4/cfg_files/demoanalyzer_' + dataset_id + '_cfg' + str(count) + '.py'
        new_output_filename = dataset_id + '_output' + str(count) + '.root'

        #Adjust the input filenames and output filename for the new cfg
        new_content = default_content
        new_content = new_content.replace('OUTPUT_FILE_STR', new_output_filename)
        new_content = new_content.replace('INPUT_FILES_STR', new_input_filenames)

        #Adjust the JSON file if the index file is for data (not necessary for MC)
        if "Run" in dataset_id:
            #Uncomment the JSON file definition lines
            new_content = new_content.replace('#goodJSON','goodJSON')
            new_content = new_content.replace('#myLumis','myLumis')

            #Adjust the JSON file depending on run year
            if "2011" in dataset_id:
                new_content = new_content.replace('INPUT_JSON_STR','json_files/Cert_160404-180252_7TeV_ReRecoNov08_Collisions11_JSON.txt')
            elif "2012" in dataset_id:
                new_content = new_content.replace('INPUT_JSON_STR','json_files/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt')

        #Create/write new cfg file using this updated content
        with open(new_filename,"w") as new_cfg:
            new_cfg.write(new_content)
