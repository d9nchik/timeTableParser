from html.parser import HTMLParser
from urllib.parse import urlencode
from urllib.request import urlopen

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


def get_text(group: str) -> str:
    link = get_link(group)
    data = urlencode({
        'ctl00_ToolkitScriptManager_HiddenField': '',
        '__VIEWSTATE': '/wEMDAwQAgAADgEMBQAMEAIAAA4BDAUDDBACAAAOAgwFBwwQAgwPAgEIQ3NzQ2xhc3MBD2J0biBidG4tcHJpbWFyeQEEXyFTQgUCAAAADAUNDBACAAAOBAwFAwwQAgwPAQEEVGV4dAEq0KDQvtC30LrQu9Cw0LQg0LfQsNC90Y/RgtGMINC00LvRjyDQhtCfLTkyAAAADAUHDBACAAAOBgwFAQwQAgAADgEMBQUMEAIMDwICAAABDWRheV9iYWNrbGlnaHQCAgAFAgAAAAwFAgwQAgAADgEMBQUMEAIMDwICAAACBQACAgAFAgAAAAwFAwwQAgAADgEMBQUMEAIMDwICAAACBQACAgAFAgAAAAwFBAwQAgAADgEMBQUMEAIMDwICAAACBQACAgAFAgAAAAwFBQwQAgAADgEMBQUMEAIMDwICAAACBQACAgAFAgAAAAwFBgwQAgAADgEMBQUMEAIMDwICAAACBQACAgAFAgAAAAwFCwwQAgAADgEMBQEMEAIAAA4BDAUBDBACDA8CAgAAAQxjbG9zZXN0X3BhaXICAgAFAgAAAAwFDQwQAgwMAA8BAQVzdHlsZQEMZmxvYXQ6cmlnaHQ7DAkQAhAFAAEb0J/QtdGA0YjQuNC5INGB0LXQvNC10YHRgtGAAQExCAgQBQABG9CU0YDRg9Cz0LjQuSDRgdC10LzQtdGB0YLRgAEBMgkIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADJEceBoHdVZlDrPNgscA8Ewup5O',
        '__EVENTTARGET': 'ctl00$MainContent$ddlSemesterType',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$ddlSemesterType': '2',
        '__EVENTVALIDATION': '/wEdAAEAAAD/////AQAAAAAAAAAPAQAAAAYAAAAIsA3rWl3AM+6E94I5ke7WZqDu1maj7tZmCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANqZqakPTbOP2+koNozn1gOvqUEW'
    })
    data = data.encode('ascii')
    answer = urlopen(link, data)
    return answer.read().decode()


def get_link(group: str) -> str:
    data = urlencode({
        '__VIEWSTATE': '/wEMDAwQAgAADgEMBQAMEAIAAA4BDAUDDBACAAAOAgwFBwwQAgwPAgEIQ3NzQ2xhc3MBD2J0biBidG4tcHJpbWFyeQEEXyFTQgUCAAAADAUNDBACAAAOAQwFAQwQAgAADgEMBQ0MEAIMDwEBBFRleHQBG9Cg0L7Qt9C60LvQsNC0INC30LDQvdGP0YLRjAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALVdjzppTCyUtNVSyV7xykGQzHz2',
        'ctl00$MainContent$ctl00$txtboxGroup': group,
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$ctl00$btnShowSchedule': 'Розклад занять',
        '__EVENTVALIDATION': '/wEdAAEAAAD/////AQAAAAAAAAAPAQAAAAUAAAAIsA3rWl3AM+6E94I5Tu9cRJoVjv0LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHfLZVQO6kVoZVPGurJN4JJIAuaU'
    })
    data = data.encode('ascii')
    answer = urlopen('http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx', data)
    return answer.url


def print_table(table, title):
    with open(NAME_OF_OUTPUT_FILE, 'a') as f:
        print('<h2 class="text-center">{}</h2>'.format(title), file=f)
        print('<table class="table table-striped table-bordered table-hover">', file=f)
        print('<thead class="thead-dark">', file=f)
        header = table[0]
        print('<tr>', file=f)
        for column in header:
            print('<th>', file=f)
            print(' '.join(column), end=' ', file=f)
            print('</th>', file=f)
        print('</tr>', file=f)
        print(file=f)
        table = table[1:]
        print('</thead><tbody>', file=f)
        for row in table:
            print('<tr>', file=f)
            for data in row:
                print('<td>', file=f)
                print(' '.join(data), end=' ', file=f)
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
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <title>MyTimeTable</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
          integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    <link rel="stylesheet" href="css/main.css">
</head>
<body>''', file=f)


def writeTailOfHTML():
    with open(NAME_OF_OUTPUT_FILE, 'a') as f:
        print('''<script src="js/main.js"></script></body></html>''', file=f)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    text = get_text('ІП-92')
    parser = MyHTMLParser()
    parser.feed(text)
    table = parser.table
    parser.close()

    first, second = split_table_on_2_week(table)
    writeHeadOfHTML()
    print_table(first, 'Перший тиждень')
    print_table(second, 'Другий тиждень')
    writeTailOfHTML()
