"""
https://parabank.parasoft.com/parabank/api-docs/index.html
"""

import requests
from lxml import etree

BASE_URI = "http://parabank.parasoft.com/parabank/services/bank"


def xml_parser(content):
    return etree.fromstring(content)


def test_get_customer(headers):
    response = requests.get(f"{BASE_URI}/customers/12212", headers=headers)
    tree = xml_parser(response.content)
    assert tree.xpath('/customer/id')[0].text == '12212'
    assert tree.xpath('/customer/firstName')[0].text == 'John'


def test_get_customer_accounts(headers):
    response = requests.get(f"{BASE_URI}/customers/12212/accounts", headers=headers)
    tree = xml_parser(response.content)
    accounts_id = tree.xpath('//id')
    for id in accounts_id:
        assert int(id.text) > 0
    account_types = ['CHECKING', 'SAVINGS', 'LOAN']
    customer_account_types = tree.xpath('//type')
    for type in customer_account_types:
        assert any(i in type.text for i in account_types)


def test_get_customer_stock_positions(headers):
    response = requests.get(f"{BASE_URI}/customers/12212/positions", headers=headers)
    tree = xml_parser(response.content)
    ids = tree.xpath('//customerId')
    for id in ids:
        assert id.text == '12212'
