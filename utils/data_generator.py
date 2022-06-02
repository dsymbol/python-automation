import random
import re
import string

import requests
from lxml import html


def numbers_generator():
    numbers = string.digits
    result_str = ''.join(random.choice(numbers) for i in range(4))
    return result_str


def person_generator():
    d = dict()

    url = "https://www.fakenamegenerator.com/gen-random-us-us.php"
    while True:
        try:
            response = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:38.0) '
                                                                'Gecko/20100101 Firefox/38.0'})
            tree = html.fromstring(response.content)
            name = tree.xpath('//div[@class="address"] /h3')[0].text
            name = name.split(" ")
            fname = name[0]
            lname = name[2]

            address = tree.xpath('//div[@class="adr"]')[0].text
            address = address.replace("\n                                        ", "")

            csp = tree.xpath('//div[@class="adr"] /br')[0].tail
            city = re.search(r"^(.*?)\,.*", csp).group(1)
            break
        except IndexError:
            continue

    for i in csp.split(" "):
        if i.isnumeric():
            zipcode = int(i)
        elif i.isalpha() and i.isupper():
            state = i

    d.update(first_name=fname, last_name=lname, address=address, city=city, state=state, zipcode=zipcode)

    fields = tree.xpath('//dl[@class="dl-horizontal"] //dt')
    values = tree.xpath('//dl[@class="dl-horizontal"] //dd')
    i = 0
    while i != len(fields):
        field = fields[i].text.lower()
        field = field.replace(" ", "_")
        value = values[i].text
        d.update({field: value})
        i += 1

    if "ssn" in d.keys():
        d["ssn"] = d["ssn"].replace("XXXX", numbers_generator())
    if "email_address" in d.keys():
        pattern = re.compile(r'\s+')
        d["email_address"] = re.sub(pattern, '', d["email_address"])

    rem_list = ["mother's_maiden_name", "qr_code", "geo_coordinates"]
    [d.pop(key) for key in rem_list]

    return d
