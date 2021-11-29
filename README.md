# TicketViewerZendesk
Web Application to view all the tickets raised<br>


Setup:<br>

1)Clone the repo
2)Install Python 3.8 and pip
3)Run this command from root 'ZendeskCC' folder: pip install -r requirements.txt
4)Run command - python manage.py makemigrations
5)Run command - python manage.py migrate


Modify values in dev.ini file as below:
tickets_api_url=https://{subdomain}.zendesk.com
api_token={your_api_token}
email_id={your_email_id}


Finally, run the command - python manage.py runserver

This will load the webapp on localhost:8000/tickets/

