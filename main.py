from urllib.request import urlopen
from html.parser import HTMLParser

URL = 'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=20eef8aa-5e2b-4225-8f05-e8fc682dc125'
NAME_OF_OUTPUT_FILE = 'index.html'


class MyHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.in_table = False
        self.table = []
        self.in_tr = False
        self.in_td = False

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'tr':
            self.table.append([])
            self.in_tr = True
        elif tag == 'td':
            self.table[-1].append([])
            self.in_td = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr':
            self.in_tr = False
        elif tag == 'td':
            self.in_td = False

    def handle_data(self, data):
        if self.in_td:
            self.table[-1][-1].append(data)


def get_text(url: str) -> str:
    text = urlopen(url).read().decode()
    return text


def print_table(table):
    with open(NAME_OF_OUTPUT_FILE, 'a') as f:
        print('<table>', file=f)
        for row in table:
            print('<tr>', file=f)
            for data in row:
                print('<td>', file=f)
                for information in data:
                    print(''.join(information), end=' ', file=f)
                print('</td>', file=f)
            print('</tr>', file=f)
            print(file=f)
        print('</table>', file=f)


def split_table_on_2_week(table):
    middle = int(len(table) / 2)
    first = table[:middle]
    second = table[middle:]
    return first, second


def writeHeadOfHTML():
    with open(NAME_OF_OUTPUT_FILE, 'w') as f:
        print('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MyTimeTable</title>
</head>
<body>''', file=f)


def writeTailOfHTML():
    with open(NAME_OF_OUTPUT_FILE, 'a') as f:
        print('''</body></html>''', file=f)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    text = get_text(URL)
    parser = MyHTMLParser()
    parser.feed(text)
    table = parser.table
    parser.close()

    first, second = split_table_on_2_week(table)
    # print_table(first)
    # print(first)
    writeHeadOfHTML()
    print_table(first)
    print_table(second)
    writeTailOfHTML()
