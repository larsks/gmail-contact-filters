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
    p.add_option('-l', '--lowercase-labels', action='store_true')
    return p.parse_args()

def main():
    opts, args = parse_args()

    max_results = int(opts.max_results)

    cf = configdict.ConfigDict('google.ini')

    # ugly hack courtesy:
    # http://code.google.com/p/gdata-python-client/issues/detail?id=230
    client = ContactsService(additional_headers={
        'GData-Version': '3'})

    # authenticate to google.
    client.ClientLogin(cf['google']['username'], cf['google']['password'])

    # get the list of contact groups.
    groups = client.GetGroupsFeed()
    selected_groups = []

    # build a list of available groups.  massage the "System group:"
    # names to be more useful.  Filter groups based on -g command
    # line option, if necessary.
    for entry in groups.entry:
        gname = entry.title.text
        if gname.startswith('System Group: '):
            gname = gname[14:]
            entry.title.text = gname

        if opts.group and not  gname in opts.group:
            continue

        selected_groups.append(entry)

    addresses={}

    # build list of addresses for each group
    for entry in selected_groups:
        addresses[entry.title.text] = []
        query = ContactsQuery(group = entry.id.text)
        query.max_results = max_results
        contacts = client.GetContactsFeed(query.ToUri())
        for contact in contacts.entry:
            for email in contact.email:
                addresses[entry.title.text].append(email.address)

    # build filter feed
    feed = filters.FilterFeed()
    for group, addrs in addresses.items():
        label = group
        if opts.lowercase_labels:
            label = label.lower()

        feed.append(filters.FilterEntry(
            'from:(%s)' % '|'.join(addrs),
            title=group,
            label=label,
            ))

    # output xml
    print feed

if __name__ == '__main__':
    main()

