from urllib.request import urlopen
from html.parser import HTMLParser

URL = 'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=20eef8aa-5e2b-4225-8f05-e8fc682dc125'
NAME_OF_OUTPUT_FILE = 'site/index.html'


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


def print_table(table, title):
    with open(NAME_OF_OUTPUT_FILE, 'a') as f:
        print('<h2 class="text-center">{}</h2>'.format(title), file=f)
        print('<table class="table table-striped table-bordered table-hover">', file=f)
        print('<thead class="thead-dark">', file=f)
        row1 = table[0]
        print('<tr>', file=f)
        for data1 in row1:
            print('<th>', file=f)
            for information1 in data1:
                print(''.join(information1), end=' ', file=f)
            print('</th>', file=f)
        print('</tr>', file=f)
        print(file=f)
        table=table[1:]
        print('</thead><tbody>', file=f)
        for row in table:
            print('<tr>', file=f)
            for data in row:
                print('<td>', file=f)
                for information in data:
                    print(''.join(information), end=' ', file=f)
                print('</td>', file=f)
            print('</tr>', file=f)
            print(file=f)
        print('</tbody></table>', file=f)


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
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
          integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    <link rel="stylesheet" href="css/main.css">
</head>
<body>''', file=f)


def writeTailOfHTML():
    with open(NAME_OF_OUTPUT_FILE, 'a') as f:
        print('''<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
        crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"
        integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN"
        crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
        integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV"
        crossorigin="anonymous"></script>
<script src="js/main.js"></script></body></html>''', file=f)


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
    print_table(first, 'Перший тиждеь')
    print_table(second, 'Другий тиждень')
    writeTailOfHTML()
