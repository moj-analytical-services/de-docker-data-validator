import os
import boto3
import gzip

from dataengineeringutils3 import s3

s3_client = boto3.client("s3")

def download_data(s3_path, local_path):
    with open(local_path, "rb") as f:
        b, o = s3.s3_path_to_bucket_key(s3_path)
        s3_client.download_fileobj(b, o, f)


def get_out_path(basepath, table, ts, filename, compress=False, filenum=0):
    filename_only, ext = filename.split(".", 1)
    final_filename = f"{filename_only}-{ts}-{filenum}.{ext}"
    if compress and not ext.endswith(".gz"):
        final_filename += ".gz"

    out_path = os.path.join(
        basepath, table, f"mojap_fileland_timestamp={ts}", final_filename
    )
    return out_path


def get_log_path(basepath, table, ts, filenum=0):
    final_filename = f"log-{table}-{ts}-{filenum}.json"

    out_path = os.path.join(basepath, table, final_filename)
    return out_path


def local_file_to_s3(local_path, s3_path):
    if (not local_path.endswith(".gz")) and (s3_path.endswith(".gz")):
        new_path = local_path + ".gz"
        with open(local_path, "rb") as f_in, gzip.open(new_path, "wb") as f_out:
            f_out.writelines(f_in)
        local_path = new_path

    b, o = s3.s3_path_to_bucket_key(s3_path)
    with open(local_path, "rb") as f:
        s3_client.upload_fileobj(f, b, o)