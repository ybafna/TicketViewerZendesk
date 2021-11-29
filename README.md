# TicketViewerZendesk
Web Application to view all the tickets raised<br>


Setup:<br>

1)Clone the repo<br>
2)Install Python 3.8 and pip<br>
3)Run this command from root 'ZendeskCC' folder: pip install -r requirements.txt<br>
4)Run command - python manage.py makemigrations<br>
5)Run command - python manage.py migrate<br>


Modify values in dev.ini file as below:<br>
tickets_api_url=https://{subdomain}.zendesk.com<br>
api_token={your_api_token}<br>
email_id={your_email_id}<br>


Finally, run the command - python manage.py runserver<br>

This will load the webapp on localhost:8000/tickets/<br>

