####Not implemented


import smtplib

from email.message import EmailMessage

def main():
    send_report_email("ifslcdb_2025-07-13T17:51:54.232904.txt")
    

def send_report_email(report):
    source="prodba_factory_internet@"
    destination="oraclechecks@pro-dba.com"
    
    # Open the plain text file whose name is in textfile for reading.
    with open(report) as fp:
    # Create a text/plain message
        email = EmailMessage()
        email.set_content(fp.read())

    email['Test Report'] = f'The contents of {report}'
    email['From'] = ""
    email['To'] = ""



if __name__ == "__main__":
    main()