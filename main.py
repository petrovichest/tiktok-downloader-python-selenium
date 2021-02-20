import os
import shutil
import time
from TikTokApi import TikTokApi
from selenium import webdriver


class TikTokParser:
    def __init__(self):
        with open('./res/bl_list.txt', 'r', encoding='utf-8') as f:
            self.urls_bl = [x.strip() for x in f.read().split('\n') if x]

        self.api = TikTokApi.get_instance()
        self.threads = 1
        self.count_of_videos = 50

    def parse_trending_urls(self):
        new_videos_url = []
        new_videos_ids = []
        count = self.count_of_videos
        print('Сбор видео')
        while True:
            videos = self.api.trending(count=count, custom_verifyFp="")
            for video in videos:
                video_id = video['id']
                if video_id in self.urls_bl:
                    continue
                video_author = video['author']['uniqueId']
                video_data = [video_id, video_author]
                new_videos_url.append(video_data)
                new_videos_ids.append(video_id)
                self.urls_bl.append(video_id)
            if  len(new_videos_ids) < self.count_of_videos:
                count += count
                continue
            with open('res/new_videos_ids.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_videos_ids))
            return new_videos_url

    def download_videos(self, browser_directory_name, urls):
        options = webdriver.ChromeOptions()
        user_path = f'{os.getcwd()}/browsers/{browser_directory_name}'
        options.add_argument(f'user-data-dir={user_path}')
        driver = webdriver.Chrome(options=options)
        print('Начинаю загрузку видео')
        for vido_data in urls:
            print(f'Заружаю видео {urls.index(vido_data) + 1} из {len(urls)}')
            video_url = f'https://www.tiktok.com/@{vido_data[1]}/video/{vido_data[0]}'

            driver.get(f'https://ttloader.com/ru/?tiktok-search={video_url}')  # Your Website Address
            for x in range(100):
                try:
                    driver.find_element_by_css_selector('[class="video-link"]').click()
                    break
                except:
                    time.sleep(.1)
            if not self.click_download_buttons(vido_data, driver):
                continue
            with open('./res/bl_list.txt', 'a', encoding='utf-8') as f:
                f.write(f'{vido_data[0]}\n')
        driver.close()

    def cleaning_the_directory(self):
        dist_files = os.listdir('./out')
        for file in dist_files:
            if not os.path.getsize(f'./out/{file}'):
                os.remove(f'./out/{file}')

    def download_videos_threads(self, urls):
        self.remove_browsers()
        self.create_browser_directories(1)
        self.download_videos(f'browser_1', urls)
        self.cleaning_the_directory()
        # for x in range(self.threads):
        #     self.create_browser_directories(x)
        #     th = Thread(target=self.download_videos, args=(f'browser_{x}', urls[x::self.threads]))
        #     th.start()
        #     time.sleep(0.1)

    def click_download_buttons(self, vido_data, driver):
        for x in range(100):
            try:
                download_button = driver.find_element_by_css_selector('[data-key="no-watermark"]')
                break
            except:
                time.sleep(.1)
        else:
            return False
        driver.get(download_button.get_attribute('href'))
        for x in range(60):
            try:
                size = os.path.getsize(f'./out/video-{vido_data[0]}-no-watermark.mp4')
                break
            except:
                time.sleep(1)
        else:
            return False
        if size == 0:
            for x in range(100):
                try:
                    download_button = driver.find_element_by_css_selector('[data-key="video"]')
                    break
                except:
                    time.sleep(.1)
            else:
                return False
            driver.get(download_button.get_attribute('href'))
            for x in range(60):
                try:
                    size = os.path.getsize(f'./out/video-{vido_data[0]}.mp4')
                    break
                except:
                    time.sleep(1)
            else:
                return False
        return True

    def create_browser_directories(self, browser_num, symlinks=False, ignore=None):
        folder_prof = f'./browsers/browser_{browser_num}'
        folder_back = './Browser_profile'
        for the_file in os.listdir(folder_back):
            s = os.path.join(folder_back, the_file)
            d = os.path.join(folder_prof, the_file)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def remove_browsers(self):
        folders = os.listdir('./browsers')
        for x in folders:
            shutil.rmtree(f'./browsers/{x}', ignore_errors=True)

    def run(self):
        urls = self.parse_trending_urls()
        self.download_videos_threads(urls)
        input('После загрузки всех видео нажать ENTER')


if __name__ == '__main__':
    pr = TikTokParser()
    pr.run()
