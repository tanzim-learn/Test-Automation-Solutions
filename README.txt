Summary
I’ve developed a small log parsing tool for NSLM that does the following:
•	Logs all exceptions across all NSLM log files that were generated during the test session only.
•	Calculates the increase in size of all log files for the test session.

How to execute:
1.	At the beginning of the test session, the script is executed as a plain python script without any inputs
python parse_nslm_session_logs.py
2.	When the testing is completed, exit the script with a keyboard interrupt :  CTRL-C

Output:
On termination, the script provides the following:
•	A dictionary containing the 
o	log file name
o	size of the file before execution
o	size of the file after execution
o	size increase during the test session
o	number of exceptions generated in the log file during the test session

Sample:
compliance-service.log': {'after_size': 13507,
                            'before_size': 13507,
                            'error_count': 0,
                            'session_size': 0},

•	A new folder “Session_Log_Excerpts”   is created which contains log excerpt files in which are logged the exceptions.
These files are created only for those NSLM log files that have exceptions generated during the test session.

Notes:
•	The script was developed with Python 3.5.2
•	It was tested to run on Linux only.
•	It runs locally on the system where NSLM server is installed. 
•	Between successive runs of the script, delete the Session_Log_Excerpts folder
