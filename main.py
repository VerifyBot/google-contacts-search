import json
import typing
import itertools

import configparser

contacts_file = 'contacts.json'

with open(contacts_file, encoding='utf8') as fp:
    contacts = json.load(fp)

new_contacts = []

def parse_phones(contact) -> typing.Optional[str]:
    phones = [
        contact['Phone 1 - Value'],
        contact['Phone 2 - Value'],
        contact['Phone 3 - Value'],
    ]

    new_phones = []

    for phone in phones:
        if not phone:
            continue

        if isinstance(phone, str):
            phone = phone.split(':::', 1)[0].strip().replace('-', '').replace('+', '').replace('972', '0')

            if not phone[0] == '0' and phone[1] == '5' and phone[0] in ['2', '3', '4', '5']:
                phone = '0' + phone

            phone = phone.replace(' ', '')

        phone = str(phone)

        # no dups
        if phone in itertools.chain(*list(map(lambda c: c['phones'], new_contacts))):
            continue

        new_phones.append(phone)

    return new_phones

for c in contacts:
    name = "{Given Name} {Additional Name} {Family Name}".format_map(c)
    name = name.replace('  ', ' ').strip()

    if not name:
        continue

    phones = parse_phones(c)

    if not phones:
        continue

    new_contacts.append(dict(
        name=name,
        phones=phones,
    ))
    # print(name, phones)

with open('parsed-contacts.json', 'w', encoding='utf8') as fp:
    json.dump(new_contacts, fp, ensure_ascii=False, indent=2)