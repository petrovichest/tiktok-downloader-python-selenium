import os
import time

from TikTokApi import TikTokApi
from scripts.file_manager import FileManager
from scripts.deemojify import deEmojify


class TikTokDownload:

    def download_by_hashtag(self, hashtag):
        api = TikTokApi.get_instance(
            custom_verifyFp=os.environ.get("verifyFp", None))
        # api = TikTokApi.get_instance()
        device_id = api.generate_device_id()

        result_count = 100
        # hashtag_objects = api.search_for_hashtags(hashtag)
        # time.sleep(5)
        tiktoks = api.by_hashtag(hashtag, custom_device_id=device_id, count=result_count)
        for one_tiktok in tiktoks:
            time.sleep(1)
            video_bytes = api.get_video_by_tiktok(one_tiktok, custom_device_id=device_id)
            FileManager().save_video(video_name=one_tiktok['id'], video_bytes=video_bytes)
            FileManager().save_video_name_and_description(f'{one_tiktok["id"]}.mp4', deEmojify(one_tiktok['desc']))


if __name__ == '__main__':
    TikTokDownload().download_by_hashtag("#бытовойлайфхак")
