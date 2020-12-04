import os
import tweepy
import urllib.request
import logging
import configparser

# 画像の保存先
BASE_DIR = os.path.join('/', 'CollectionFromTwitter')
os.makedirs(BASE_DIR, exist_ok=True)

# loggingの設定
LOG_FILE = os.path.join(BASE_DIR, 'image_collect.log')

# Twitter APIを実行する変数を保存したconfig.iniファイルをロード
CONFIG_INI_FILE = 'config.ini'
config_ini = configparser.ConfigParser()

if not os.path.exists(CONFIG_INI_FILE):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), CONFIG_INI_FILE)

config_ini.read(CONFIG_INI_FILE, encoding='utf-8')

CONSUMER_KEY = config_ini['TWITTER_API']['CONSUMER_KEY']
CONSUMER_SECRET = config_ini['TWITTER_API']['CONSUMER_SECRET']
ACCESS_TOKEN_KEY =config_ini['TWITTER_API']['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = config_ini['TWITTER_API']['ACCESS_TOKEN_SECRET']

class CollectionImages:
    _accounts = list()
    _api = None
    _img_dir = None

    def __init__(self):
        """初期設定
        """
        self.set_api()
        self.set_search_account()

    def set_api(self):
        """apiの設定
        """
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        self._api = tweepy.API(auth)

    def set_search_account(self):
        self._accounts.append('TwitterJP')

    def run(self):
        """
        1. 対象のアカウントをサーチ。20件ほど取得
        2. mediaがあったら画像を取得して保存
        3. 1,2を登録したアカウントの数だけ繰り返す
        :return:
        """
        for a in self._accounts:
            timeline = self._api.user_timeline(screen_name=a, count=20)
            for t in timeline:
                created_at = t.created_at
                if 'media' in t.entities:
                    self._img_dir = os.path.join(BASE_DIR, a)
                    status = self._api.get_status(t.id)
                    for i, s in enumerate(
                            status.extended_entities['media']):
                        self.download(s['media_url'], i, created_at)


    def download(self, url, num, created_at):
        """画像のダウンロード
        """
        os.makedirs(self._img_dir, exist_ok=True)

        url_orig = '%s:orig' % url
        img_name = '{0}-{1}_{2}'.\
            format(created_at.strftime('%Y%m%d'), num, url.split('/')[-1])
        path = os.path.join(self._img_dir, img_name)
        if not os.path.isfile(path):
            try:
                response = urllib.request.urlopen(url=url_orig)
                with open(path, "wb") as f:
                    f.write(response.read())
            except Exception as e:
                logging.warning(' Download Failed:{0}, {1}'.format(url, error))
            else:
                logging.info(' Download Success:{0}'.format(path))


def main():
    """メイン処理
    """
    try:
        logging.basicConfig(filename=LOG_FILE, format='%(levelname)s:%(asctime)s %(message)s',
                            level=logging.INFO)
        downloader = CollectionImages()
        downloader.run()

    except KeyboardInterrupt:
        # Ctrl-Cで終了
        pass


if __name__ == '__main__':
    main()
