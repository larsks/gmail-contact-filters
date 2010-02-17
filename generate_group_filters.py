import os
import sys
import optparse

import configdict
from gdata.contacts.service import ContactsService, ContactsQuery

def parse_args():
    p = optparse.OptionParser()
    p.add_option('-f', '--config', default='google.ini')
    p.add_option('-g', '--group', action='append')
    p.add_option('-m', '--max-results', default='200')
    return p.parse_args()

def main():
    opts, args = parse_args()

    max_results = int(opts.max_results)

    cf = configdict.ConfigDict('google.ini')
    client = ContactsService(additional_headers={
        'GData-Version': '2'})
    client.ClientLogin(cf['google']['username'], cf['google']['password'])

    groups = client.GetGroupsFeed()
    selected_groups = []

    for entry in groups.entry:
        gname = entry.title.text
        gname_short = gname
        if gname.startswith('System Group: '):
            gname_short = gname[14:]

        if opts.group and not (
                gname in opts.group or gname_short in opts.group):
            continue

        selected_groups.append(entry)

    addresses={}

    for entry in selected_groups:
        addresses[entry.title.text] = []
        query = ContactsQuery(group = entry.id.text)
        query.max_results = max_results
        contacts = client.GetContactsFeed(query.ToUri())
        for contact in contacts.entry:
            for email in contact.email:
                addresses[entry.title.text].append(email.address)

    for group, addrs in addresses.items():
        print '#', group
        print 'from:(%s)' % '|'.join(addrs)
        print

if __name__ == '__main__':
    main()

