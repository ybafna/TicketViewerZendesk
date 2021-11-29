import configparser
from unittest.mock import patch

from django.test import TestCase

# Create your tests here.
from Tickets.models import Ticket
from Tickets.views import get_auth_token, get_headers, get_all_tickets, get_ticket


class MockIndividualTicketDataFailure:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            'error': 'Some error'
        }


class MockIndividualTicketFailure:
    def __init__(self):
        self.status_code = 500

    def json(self):
        return None


class MockIndividualTicket:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            "ticket":
                {
                    "assignee_id": 111111,
                    "collaborator_ids": [
                        35334,
                        234
                    ],
                    "created_at": "2009-07-20T22:55:29Z",
                    "custom_fields": [
                        {
                            "id": 27642,
                            "value": "745"
                        },
                        {
                            "id": 27648,
                            "value": "yes"
                        }
                    ],
                    "description": "The fire is very colorful.",
                    "due_at": None,
                    "external_id": "ahg35h3jh",
                    "follower_ids": [
                        35334,
                        234
                    ],
                    "group_id": 98738,
                    "has_incidents": False,
                    "id": 40000,
                    "organization_id": 509974,
                    "priority": "high",
                    "problem_id": 9873764,
                    "raw_subject": "{{dc.printer_on_fire}}",
                    "recipient": "support@company.com",
                    "requester_id": 20978392,
                    "satisfaction_rating": {
                        "comment": "Great support!",
                        "id": 1234,
                        "score": "good"
                    },
                    "sharing_agreement_ids": [
                        84432
                    ],
                    "status": "open",
                    "subject": "Help, my printer is on fire!",
                    "submitter_id": 76872,
                    "tags": [
                        "enterprise",
                        "other_tag"
                    ],
                    "type": "incident",
                    "updated_at": "2011-05-05T10:38:52Z",
                    "url": "https://company.zendesk.com/api/v2/tickets/35436.json",
                    "via": {
                        "channel": "web"
                    }
                }
        }


class MockResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            "tickets": [
                {
                    "assignee_id": 235323,
                    "collaborator_ids": [
                        35334,
                        234
                    ],
                    "created_at": "2009-07-20T22:55:29Z",
                    "custom_fields": [
                        {
                            "id": 27642,
                            "value": "745"
                        },
                        {
                            "id": 27648,
                            "value": "yes"
                        }
                    ],
                    "description": "The fire is very colorful.",
                    "due_at": None,
                    "external_id": "ahg35h3jh",
                    "follower_ids": [
                        35334,
                        234
                    ],
                    "group_id": 98738,
                    "has_incidents": False,
                    "id": 35436,
                    "organization_id": 509974,
                    "priority": "high",
                    "problem_id": 9873764,
                    "raw_subject": "{{dc.printer_on_fire}}",
                    "recipient": "support@company.com",
                    "requester_id": 20978392,
                    "satisfaction_rating": {
                        "comment": "Great support!",
                        "id": 1234,
                        "score": "good"
                    },
                    "sharing_agreement_ids": [
                        84432
                    ],
                    "status": "open",
                    "subject": "Help, my printer is on fire!",
                    "submitter_id": 76872,
                    "tags": [
                        "enterprise",
                        "other_tag"
                    ],
                    "type": "incident",
                    "updated_at": "2011-05-05T10:38:52Z",
                    "url": "https://company.zendesk.com/api/v2/tickets/35436.json",
                    "via": {
                        "channel": "web"
                    }
                },
                {
                    "assignee_id": 435231,
                    "collaborator_ids": [
                        35334,
                        234
                    ],
                    "created_at": "2009-07-20T22:55:29Z",
                    "custom_fields": [
                        {
                            "id": 27642,
                            "value": "745"
                        },
                        {
                            "id": 27648,
                            "value": "yes"
                        }
                    ],
                    "description": "The fire is very colorful.",
                    "due_at": None,
                    "external_id": "ahg35h3jh",
                    "follower_ids": [
                        35334,
                        234
                    ],
                    "group_id": 98738,
                    "has_incidents": False,
                    "id": 35437,
                    "organization_id": 509974,
                    "priority": "high",
                    "problem_id": 9873764,
                    "raw_subject": "{{dc.printer_on_fire}}",
                    "recipient": "support@company.com",
                    "requester_id": 20978392,
                    "satisfaction_rating": {
                        "comment": "Great support!",
                        "id": 1234,
                        "score": "good"
                    },
                    "sharing_agreement_ids": [
                        84432
                    ],
                    "status": "open",
                    "subject": "Help, my printer is on fire!",
                    "submitter_id": 76872,
                    "tags": [
                        "enterprise",
                        "other_tag"
                    ],
                    "type": "incident",
                    "updated_at": "2011-05-05T10:38:52Z",
                    "url": "https://company.zendesk.com/api/v2/tickets/35436.json",
                    "via": {
                        "channel": "web"
                    }
                }
            ]
        }


class CustomConfig(configparser.ConfigParser):
    def __getitem__(self, key):
        if key == 'DEFAULT':
            return {'all_tickets_url_path': '/api/v2/tickets.json',
                    'individual_ticket_url_path': '/api/v2/tickets',
                    'tickets_api_url': 'https://abc.zendesk.com',
                    'api_token': 'abcdxyz123',
                    'email_id': 'abc@gmail.com',
                    }
        else:
            raise KeyError(str(key))


class TicketsTestCase(TestCase):
    def setUp(self):
        for ticket in Ticket.objects.all():
            ticket.objects.get(id=ticket.id).delete()

    def test_auth_token(self):
        config = configparser.ConfigParser()
        config.set('DEFAULT', 'email_id', 'abc@gmail.com')
        config.set('DEFAULT', 'api_token', 'abcdxyz123')
        self.assertEqual(get_auth_token(config), 'YWJjQGdtYWlsLmNvbS90b2tlbjphYmNkeHl6MTIz')

    def test_headers(self):
        config = configparser.ConfigParser()
        config.set('DEFAULT', 'email_id', 'abc@gmail.com')
        config.set('DEFAULT', 'api_token', 'abcdxyz123')
        headers = get_headers(config)
        self.assertEqual(headers.get('Authorization'), 'Basic YWJjQGdtYWlsLmNvbS90b2tlbjphYmNkeHl6MTIz')

    @patch("requests.get", return_value=MockResponse())
    @patch('configparser.ConfigParser', side_effect=CustomConfig)
    def test_get_all_tickets(self, mock_response, config_parser):
        get_all_tickets(None)
        self.assertEquals(len(Ticket.objects.all()), 2)
        self.assertIsNotNone(Ticket.objects.get(id=35436))
        self.assertEquals(Ticket.objects.get(id=35436).assignee_id, 235323)
        self.assertEquals(Ticket.objects.get(id=35437).assignee_id, 435231)

    @patch("requests.get", return_value=MockIndividualTicket())
    @patch('configparser.ConfigParser', side_effect=CustomConfig)
    def test_get_individual_ticket_success(self, mock_response, config_parser):
        ticket2 = get_ticket(ticket_id=str(40000))
        self.assertIsNotNone(ticket2)
        self.assertEquals(ticket2.assignee_id, 111111)

    @patch("requests.get", return_value=MockIndividualTicketFailure())
    @patch('configparser.ConfigParser', side_effect=CustomConfig)
    def test_get_individual_ticket_api_error(self, mock_response, config_parser):
        ticket = get_ticket(ticket_id=str(12345))
        self.assertIsNotNone(ticket)
        self.assertEquals(ticket['error'], 'API Failure')

    @patch("requests.get", return_value=MockIndividualTicketDataFailure())
    @patch('configparser.ConfigParser', side_effect=CustomConfig)
    def test_get_individual_ticket_data_error(self, mock_response, config_parser):
        ticket = get_ticket(ticket_id=str(12345))
        self.assertIsNotNone(ticket)
        self.assertEquals(ticket['error'], 'API Failure')
