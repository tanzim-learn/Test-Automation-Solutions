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

import re, os, pprint, datetime, time, sys


##########################
# Variable Declaration
##########################
log_folder_path = "/var/log/apiserver" #apiservices log folder path
log_file_list = []
log_summary_dict = {} 			#dictionary to hold log analysis summary 
log_summary_folder_path = "./Session_Log_Excerpts" #folder to hold the extracted log contents
#[DONE]TBD : get timestamp of the system when the script is invoked  
now = datetime.datetime.now()


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
    check = True
    num_of_errors=0
    log_file_dict[file_name]['error_count'] = 0	

    for lines in log_file_read:
    #[DONE]TBD - get current timestamp passed to function. Compare each line timestamp and find the first line greater than or equal to current timestamp. Parse all lines for error after that
        mo = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', lines)
        if mo != None:
            log_timestamp = mo.group()

        [date_pattern, time_pattern] = log_timestamp.split()
        [tyear, tmonth, tday] = date_pattern.split('-')
        [thour, tminute, tsecond] = time_pattern.split(':')

        log_time = now.replace(year=int(tyear), month=int(tmonth), day=int(tday), hour=int(thour), minute=int(tminute),
                                   second=int(tsecond))
        if log_time <= now and check == True:
            continue

        check = False
        log_file_dict[file_name]['error_count'] = 0
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
                    log_file_dict[file_name]['error_count'] = num_of_errors



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
    if os.path.isdir(log_summary_folder_path):
        #os.rmdir(log_summary_folder_path)
	os.system("rm -rf " +log_summary_folder_path)


    os.makedirs(log_summary_folder_path)	

    # List all .log files only
    for file in log_file_list_all:
        #print ("File : " +file)
        file_match_obj = re.compile(r'log$')
        mo = file_match_obj.search(file)
        if mo != None:
            log_file_list.append(file)

    #Create dictionary with log file names as keys -> size as value   
    print ("\nThe following log files will be parsed for Error messages : \n")	
    for file in log_file_list:
        print (file)
        log_summary_dict[file] = {}
        log_summary_dict[file]['before_size'] = os.path.getsize(log_folder_path+"/"+file)
       
	#[DONE]TBD - put blank code in infinite while loop
	#[DONE]TBD - put parse code in except keyboardinterrupt
	#[DONE]TBD - put log_summary_dict pprint in except code 
	#[DONE]TBD - calulate after size and difference in size



    while True:
        try:
            print ("\nCTRL-C if your test is done\n")
            time.sleep(30)
            
        except KeyboardInterrupt:
            #print ("\nCaught Keyboard Interrupt!\n")
	    print ("\n\nData being processed.\n")	

            for file in log_file_list:
                #print ("\nFILE NAME : \n" +file)

                log_summary_dict[file]['after_size']  = os.path.getsize(log_folder_path+"/"+file)
                log_summary_dict[file]['session_size'] = log_summary_dict[file]['after_size'] - log_summary_dict[file]['before_size']

                if file == 'install.log':
                    continue

                log_summary_dict = parse_file(log_folder_path,file, log_summary_dict)   
            
            pprint.pprint(log_summary_dict)
	    print ("\nLog excerpts for log files having errors are placed at : " +log_summary_folder_path)	

            sys.exit()
        
else:
    print ("Directory does not exist : " +log_folder_path)

