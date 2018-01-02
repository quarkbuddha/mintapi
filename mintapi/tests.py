import copy
import datetime
import json
import unittest
from unittest.mock import patch

import mintapi
import mintapi.api

accounts_example = [{
    "accountName": "Chase Checking",
    "lastUpdated": 1401201492000,
    "lastUpdatedInString": "25 minutes",
    "accountType": "bank",
    "currentBalance": 100.12,
}]


class MintApiTests(unittest.TestCase):
    @patch.object(mintapi.api, 'get_web_driver')
    def test_accounts(self, mock_driver):
        token_json = json.dumps({'token': '123'})
        mock_driver.return_value.find_element_by_name.return_value.get_attribute.return_value = token_json

        accounts_json = json.dumps({'response': {'42': {'response': accounts_example}}})
        mock_driver.return_value.request.return_value.text = accounts_json

        accounts = mintapi.get_accounts('foo', 'bar')

        self.assertFalse('lastUpdatedInDate' in accounts)
        self.assertNotEqual(accounts, accounts_example)

        accounts_annotated = copy.deepcopy(accounts_example)
        for account in accounts_annotated:
            account['lastUpdatedInDate'] = (datetime.datetime.fromtimestamp(account['lastUpdated'] / 1000))
        self.assertEqual(accounts, accounts_annotated)

        # ensure everything is json serializable as this is the command-line
        # behavior.
        mintapi.print_accounts(accounts)
