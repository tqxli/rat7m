import os
import urllib.request

video_urls = [
    'https://figshare.com/ndownloader/articles/13751023/versions/1',
    'https://figshare.com/ndownloader/articles/13753417/versions/1',
    'https://figshare.com/ndownloader/articles/13759336/versions/1',
    'https://figshare.com/ndownloader/articles/13764208/versions/1',
    'https://figshare.com/ndownloader/articles/13767502/versions/2',
    'https://figshare.com/ndownloader/articles/13770565/versions/1',
    'https://figshare.com/ndownloader/articles/13769833/versions/1'
]
annot_url = 'https://figshare.com/ndownloader/articles/13739233/versions/2'
exps = ['s1-d1', 's2-d1', 's2-d2', 's3-d1', 's4-d1', 's5-d1', 's5-d2']

# create video sequence output dir
os.makedirs('video_sequences', exist_ok=True)

# download videos from urls
for url, exp in zip(video_urls):
    urllib.request.urlretrieve(url, os.path.join('video_sequences', '{}.zip'.format(exp)))

# unzipping


