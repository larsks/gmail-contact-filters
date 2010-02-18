import os
import sys
import optparse

import filters
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
        if gname.startswith('System Group: '):
            gname = gname[14:]
            entry.title.text = gname

        if opts.group and not  gname in opts.group:
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

    feed = filters.FilterFeed()
    for group, addrs in addresses.items():
        feed.append(filters.FilterEntry(
            'from:(%s)' % '|'.join(addrs),
            title=group,
            label=group,
            ))

    print feed

if __name__ == '__main__':
    main()

