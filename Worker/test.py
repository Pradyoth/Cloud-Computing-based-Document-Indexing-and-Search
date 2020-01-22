from google.cloud import storage
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
gcs = storage.client()
bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
files = bucket.list_blobs()
for file in files:
    print(file)