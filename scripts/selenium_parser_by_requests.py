import json

from seleniumwire import webdriver
from seleniumwire.utils import decode



class SeleniumParserByRequests:

    def run(self):
        self.driver = webdriver.Chrome()

        self.driver.get('https://www.tiktok.com/search?q=девушка&t=1639399187409')



        events = self.driver.requests
        for event in events:
            try:
                event.url
            except:
                continue
            if 'https://www.tiktok.com/node/share/discover/list' in event.url:
                if event.response:
                    try:
                        # addresses_bytes = event.response.body
                        response_bytes = decode(event.response.body, event.response.headers.get('Content-Encoding', 'identity'))
                        response_json = json.loads(response_bytes.decode(), strict=False)
                    except:
                        continue
                    print(response_json)


if __name__ == '__main__':
    SeleniumParserByRequests().run()