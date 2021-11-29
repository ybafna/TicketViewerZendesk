# TicketViewerZendesk
Web Application to view all the tickets raised<br>


Setup:<br>

1)Clone the repo<br>
2)Install Python 3.8 and pip<br>
3)Run the following commands in sequence from root 'ZendeskCC' folder: <br>
pip install -r requirements.txt<br>
python manage.py makemigrations<br>
python manage.py migrate<br>


Modify values in dev.ini file as below:<br>
tickets_api_url=https://{subdomain}.zendesk.com<br>
api_token={your_api_token}<br>
email_id={your_email_id}<br>


Finally, run the command - python manage.py runserver<br>

Now you may hit the url http://localhost:8000/tickets/ to view all the tickets.<br>
