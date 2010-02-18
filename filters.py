from xml.etree import ElementTree as ET

NS_ATOM = 'http://www.w3.org/2005/Atom'
NS_GAPPS = 'http://schemas.google.com/apps/2006'

class FilterFeed(list):

    def feed(self):
        feed = ET.Element('{%s}feed' % NS_ATOM)
        ET.SubElement(feed, '{%s}title' % NS_ATOM).text = 'Mail Filters'
        ET.SubElement(feed, '{%s}id' % NS_ATOM)
        ET.SubElement(feed, '{%s}updated' % NS_ATOM)
        author = ET.SubElement(feed, '{%s}author' % NS_ATOM)
        ET.SubElement(author, '{%s}name' % NS_ATOM)
        ET.SubElement(author, '{%s}email' % NS_ATOM)

        for entry in self:
            feed.append(entry.entry())

        return feed

    def __str__(self):
        return ET.tostring(self.feed())

class FilterEntry(object):

    def __init__ (self, filterString,
            title='Mail Filter',
            shouldArchive=False,
            shouldMarkAsRead=False,
            label=None,
            forwardTo=None):
        self.filterString = filterString
        self.shouldArchive = shouldArchive
        self.shouldMarkAsRead = shouldMarkAsRead
        self.title = title
        self.label=label
        self.forwardTo=None

    def entry(self):
        entry = ET.Element('{%s}entry' % NS_ATOM)

        ET.SubElement(entry, '{%s}category' % NS_ATOM,
                { 'term': 'filter' })
        ET.SubElement(entry, '{%s}title' % NS_ATOM).text = self.title
        ET.SubElement(entry, '{%s}id' % NS_ATOM)
        ET.SubElement(entry, '{%s}content' % NS_ATOM)
        ET.SubElement(entry, '{%s}updated' % NS_ATOM)
        ET.SubElement(entry, '{%s}property' % NS_GAPPS,
                {'name': 'hasTheWord',
                    'value': self.filterString})

        if self.shouldMarkAsRead:
            ET.SubElement(entry, '{%s}property' % NS_GAPPS,
                    {'name': 'shouldMarkAsRead',
                        'value': 'true'})

        if self.shouldArchive:
            ET.SubElement(entry, '{%s}property' % NS_GAPPS,
                    {'name': 'shouldArchive',
                        'value': 'true'})

        if self.label:
            ET.SubElement(entry, '{%s}property' % NS_GAPPS,
                    {'name': 'label',
                        'value': self.label})

        if self.forwardTo:
            ET.SubElement(entry, '{%s}property' % NS_GAPPS,
                    {'name': 'forwardTo',
                        'value': self.forwardTo})


        return entry

    def __str__(self):
        return ET.tostring(self.entry())

