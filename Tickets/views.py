import requests
from django.shortcuts import render
import base64
import configparser
import os
import datetime
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
from Tickets.models import Ticket


# View that handle request for fetching all the tickets for a user
def get_tickets(request):
    """ If data is already present in the DB, use it, else make an API call to fetch all the tickets.
    The idea behind this is the assumption that ticket data does not change frequently.
    So, to avoid API calls everytime the user wants to see his tickets,
    we can rather used a scheduled job that updates the DB after certain interval, for eg. 1 day or 1 hour depending on how frequently the tickets get updated.

    This logic can be modified as per the requirements
    """
    try:
        if not Ticket.objects.all():
            tickets_all = get_all_tickets(request)
        # tickets_all = Ticket.objects.all()
        if 'error' not in tickets_all:
            page = request.GET.get('page', 1)

            # Divides response into pages with 25 elements in each page
            paginated_tickets = Paginator(tickets_all, 25)
            try:
                tickets = paginated_tickets.page(page)
            except PageNotAnInteger:
                tickets = paginated_tickets.page(1)
            except EmptyPage:
                tickets = paginated_tickets.page(paginated_tickets.num_pages)
            return render(request=request, template_name='index.html', context={'tickets': tickets}, status=200)
        else:
            return render(request=request, template_name='error.html',
                          context={'tickets': tickets_all, 'error_code':tickets_all['error_code']}, status=200)
    except Exception:
        logging.info("Error :: Get Tickets")
        return render(request=request, template_name='error.html', context={'error_code': 500}, status=500)


def get_individual_ticket(request, ticket_id):
    """Retrieve individual ticket details.
    If present in DB, return it, else fetch from API and save it to DB.
    It may happen that some tickets exist, but are not present in DB as we are updating the DB after certain intervals.
    In such cases, save it to the DB, until DB refresh happens.
    This logic can be modified as per the requirements.
    """
    try:
        if Ticket.objects.filter(id=ticket_id).exists():
            ticket_data = Ticket.objects.get(id=ticket_id)
            return render(request=request, template_name='ticket_detail.html',
                          context={'ticket_data': ticket_data, 'ticket_id': ticket_id}, status=200)
        else:
            ticket_data = get_ticket(ticket_id)
            if 'error' not in ticket_data:
                return render(request=request, template_name='ticket_detail.html',
                              context={'ticket_data': ticket_data, 'ticket_id': ticket_id}, status=200)
            else:
                return render(request=request, template_name='error.html',
                              context={'ticket_data': ticket_data, 'ticket_id': ticket_id,
                                       'error_code': ticket_data['error_code']}, status=200)
    except Exception:
        logging.info("Error :: Get Individual Ticket")
        return render(request=request, template_name='error.html', context={'error_code': 500}, status=500)


def get_ticket(ticket_id):
    config = get_config('dev.ini')
    headers = get_headers(config)
    base_api_url = config['DEFAULT']['tickets_api_url']
    individual_ticket_url_path = config['DEFAULT']['individual_ticket_url_path']
    response = requests.get(base_api_url + individual_ticket_url_path + "/" + ticket_id, headers=headers)
    # If API response is successful and does not contain any error, save the ticket to DB and return
    if response.status_code == 200 and 'ticket' in response.json():
        if Ticket.objects.filter(id=ticket_id).exists():
            Ticket.objects.get(id=ticket_id).delete()
        parse_ticket_object(response.json()['ticket'])
        ticket_data = Ticket.objects.get(id=ticket_id)
    else:
        # Can be broken further into different HTTP codes as per the requirement
        ticket_data = create_error_response(response.status_code)

    return ticket_data


def create_error_response(error_code):
    response = {
        'error': 'API Failure',
        'error_code': error_code

    }
    return response


# Fetches tickets from Zendesk Ticket API
def get_all_tickets(request):
    config = get_config('dev.ini')
    headers = get_headers(config)

    base_api_url = config['DEFAULT']['tickets_api_url']
    all_tickets_url_path = config['DEFAULT']['all_tickets_url_path']
    response = requests.get(base_api_url + all_tickets_url_path, headers=headers)
    # Check if API response
    if response.status_code == 200:
        json_response = response.json()
        if 'tickets' in json_response:
            # Parses the response object and saves in DB
            for ticket in json_response['tickets']:
                parse_ticket_object(ticket)
    else:
        return create_error_response(response.status_code)
    return Ticket.objects.all()


# Creates headers for API call
def get_headers(config):
    token = get_auth_token(config)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + token,
        'Accept': 'application/json'
    }

    return headers


# Saves all the relevant information from the API response to DB
def parse_ticket_object(ticket_json):
    ticket = Ticket()
    ticket.assignee_id = ticket_json['assignee_id']
    ticket.id = ticket_json['id']
    ticket.created_at = datetime.datetime.strptime(ticket_json['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    ticket.updated_at = datetime.datetime.strptime(ticket_json['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
    ticket.type = ticket_json['type']
    ticket.subject = ticket_json['subject']
    ticket.raw_subject = ticket_json['raw_subject']
    ticket.description = ticket_json['description']
    ticket.priority = ticket_json['priority']
    ticket.status = ticket_json['status']
    ticket.recipient = ticket_json['recipient']
    ticket.status = ticket_json['status']
    ticket.requester_id = ticket_json['requester_id']
    ticket.submitter_id = ticket_json['submitter_id']
    ticket.assignee_id = ticket_json['assignee_id']
    ticket.due_at = ticket_json['due_at']
    ticket.tags = ticket_json['tags']

    ticket.save()


# Read properties file
def get_config(file_name):
    path = os.path.dirname(os.path.realpath(__file__))
    config_dir = '/'.join([path, file_name])
    config = configparser.ConfigParser()
    config.read(config_dir)
    return config


# Generating Token for API authentication
def get_auth_token(config):
    email_id = config['DEFAULT']['email_id']
    api_token = config['DEFAULT']['api_token']
    auth = email_id + "/token:" + api_token
    base64_bytes = base64.b64encode(auth.encode('ascii'))
    token = base64_bytes.decode('ascii')
    return token
