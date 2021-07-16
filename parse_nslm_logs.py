#!/usr/bin/python

'''
SCRIPT SUMMARY
--------------
This script will parse the NSLM log files and provide the following data:

*Per Log file
**Exception types, number of each exception and timestamp
**Spam detection
**Size of the log file
**Diff in file size before and after test

SCRIPT FEATURES
---------------
1: Spam detection
2: Run continuously in the background
3: Mail Notifications
4: Handle file roll over
5: Provide logs between specified timestamps
6: Provide logs of specified log level

'''

import re, os, pprint




##########################
# Variable Declaration
##########################
log_folder_path = "/var/log/apiserver" #apiservices log folder path
log_file_list = []
log_summary_dict = {} 			#dictionary to hold log analysis summary 
log_summary_folder_path = "./Log_Excerpts" #folder to hold the extracted log contents
 


##########################
# Functions
##########################


'''

parse_log_file : Function parses the log file for errors
		 Creates an excerpt log files and logs errors from the log file to it.

'''


def parse_file (log_path,file_name,log_file_dict):
    log_file_obj = open(log_path + "/" +file_name)
    log_file_read = log_file_obj.readlines()
    num_of_errors=0 
    for lines in log_file_read:
        mo = re.search(r'.*ERROR.*',lines)
        if mo !=None:
 	        #print ("ERROR LINE : " + mo.group())
                
                #Create/Append to log-excerpt file
                log_excerpt_file_obj = open( log_summary_folder_path + '/' + file_name + '_excerpt','a')
                
                log_excerpt_file_obj.write(lines + "\n")
                
                #Close file
                log_excerpt_file_obj.close()    
                num_of_errors = num_of_errors + 1
                #Increment error count in log_file_dict
                log_file_dict[file_name]['error_num'] = num_of_errors
        


    #close log file
    log_file_obj.close()
    return log_file_dict



#########################
# Main Code 
#########################


# Check if the folder '/var/log/apiserver/' exists
if os.path.isdir(log_folder_path):
    print ("Directory exists : " +log_folder_path)
    log_file_list_all = os.listdir(log_folder_path)
	
    # Create sub log directory
    os.makedirs(log_summary_folder_path)	
    # List all .log files only
    for file in log_file_list_all:
        #print ("File : " +file)
        file_match_obj = re.compile(r'log$')
        mo = file_match_obj.search(file)
        if mo != None:
            log_file_list.append(file)

    #Create dictionary with log file names as keys -> size as value    
    for file in log_file_list:
        print (file)
        log_summary_dict[file] = {}
        log_summary_dict[file]['before_size'] = os.path.getsize(log_folder_path+"/"+file)
        
        log_summary_dict = parse_file(log_folder_path,file, log_summary_dict)
    
    pprint.pprint(log_summary_dict)
        
else:
    print ("Directory does not exist : " +log_folder_path)











