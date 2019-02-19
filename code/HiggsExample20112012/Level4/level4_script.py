#Open file that contains list of sample datasets
with open("List_indexfile.txt","r") as fi:
    samples = []
    #Read line by line
    for line in fi:
        #Only interested in lines that start with filepath
        if line.startswith('/'):
            #Remove the empty first element and the AOD or AODSIM last element
            samples.append(line.split('/')[1:-1])


################################################################################
import glob

#Get pathnames to all the .txt index files from within the datasets directory
datasets = glob.glob('datasets/*.txt', recursive=True)

#Read in the default format for the python configuration files
with open('code/HiggsExample20112012/Level4/default_cfg.py', 'r') as default_cfg:
    default_content = default_cfg.read()

N = 10      #Max Number of rootfiles to be input to each newly generated cfg file
count = 0   #Make a count to keep track the number of cfg files generated

#Iterate through each of the index files listed within the datasets array
for index_filename in datasets:
    with open(index_filename,"r") as index_file:

        #Read in the index file and create list of each line without '\n'
        lines = index_file.read().splitlines()

        #Iterate through each N set of lines
        for i in range(0, len(lines), N):
            #Get new list of N root files
            N_rootfiles = lines[i:i+N]

            #Turn this list of N root files into 1 string delimited with commas
            new_input_filenames = ','.join(N_rootfiles)

            #Update the count and create the new cfg filename and the new output filename
            count += 1
            new_filename = 'code/HiggsExample20112012/Level4/cfg_files/demoanalyzer_cfg' + str(count) + '.py'
            new_output_filename = 'output' + str(count) + '.root'

            #Adjust the input filenames and output filename for the new cfg
            new_content = default_content
            new_content = new_content.replace('OUTPUT_FILE_STR', new_output_filename)
            new_content = new_content.replace('INPUT_FILES_STR', new_input_filenames)

            #Adjust the JSON file if the index file is for data (not necessary for MC)
            if "Run" in index_filename:
                #Uncomment the JSON file definition lines
                new_content = new_content.replace('#goodJSON','goodJSON')
                new_content = new_content.replace('#myLumis','myLumis')

                #Adjust the JSON file depending on run year
                if "2011" in index_filename:
                    new_content = new_content.replace('INPUT_JSON_STR','json_files/Cert_160404-180252_7TeV_ReRecoNov08_Collisions11_JSON.txt')
                elif "2012" in index_filename:
                    new_content = new_content.replace('INPUT_JSON_STR','json_files/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt')

            #Create/write new cfg file using this updated content
            with open(new_filename,"w") as new_cfg:
                new_cfg.write(new_content)
