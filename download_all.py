import os
import urllib.request
import zipfile

VIDEO_URLS = [
    'https://figshare.com/ndownloader/articles/13751023/versions/1',
    'https://figshare.com/ndownloader/articles/13753417/versions/1',
    'https://figshare.com/ndownloader/articles/13759336/versions/1',
    'https://figshare.com/ndownloader/articles/13764208/versions/1',
    'https://figshare.com/ndownloader/articles/13767502/versions/2',
    'https://figshare.com/ndownloader/articles/13770565/versions/1',
    'https://figshare.com/ndownloader/articles/13769833/versions/1'
]
ANNOT_URL = 'https://figshare.com/ndownloader/articles/13739233/versions/2'
EXP_NAMES = ['s1-d1', 's2-d1', 's2-d2', 's3-d1', 's4-d1', 's5-d1', 's5-d2']

# create output dirs
os.makedirs('video_sequences', exist_ok=True)
os.makedirs('zips', exist_ok=True)

# download videos and unzip
for url, exp in zip(VIDEO_URLS, EXP_NAMES):
    zip_dir = os.path.join('zips', '{}.zip'.format(exp))
    print("Downloading videos for experiment {} ...".format(exp))
    urllib.request.urlretrieve(url, zip_dir)
    print("Unzipping video sequences ...")
    with zipfile.ZipFile(zip_dir, 'r') as zip_ref:
        zip_ref.extractall('video_sequences')

# download annotations and unzip
annot_dir = os.path.join('zips', 'annot.zip')
print("Downloading annotations ...")
urllib.request.urlretrieve(ANNOT_URL, annot_dir)
print("Unzipping annotations ...")
with zipfile.ZipFile(annot_dir, 'r') as zip_ref:
    zip_ref.extractall('annotations')


