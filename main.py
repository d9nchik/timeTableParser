from urllib.request import urlopen
from html.parser import HTMLParser

URL = 'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=20eef8aa-5e2b-4225-8f05-e8fc682dc125'


class MyHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.in_table = False
        self.table = []
        self.in_tr = False
        self.in_td = False

    def handle_starttag(self, tag, attrs):
        if tag == 'table' or self.in_table:
            self.in_table = True
            print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        if self.in_table:
            print("Encountered an end tag :", tag)
        if tag == 'table':
            self.in_table = False


    def handle_data(self, data):
        if self.in_table:
            print("Encountered some data  :", data)


def get_text(url: str) -> str:
    text = urlopen(url).read().decode()
    return text


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    text = get_text(URL)
    parser = MyHTMLParser()
    parser.feed(text)
    parser.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
