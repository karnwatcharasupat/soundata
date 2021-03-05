import argparse
import hashlib
import json
import os
import glob

INDEX_PATH = "../soundata/datasets/indexes/urbansound8k_index.json"


def md5(file_path):
    """Get md5 hash of a file.

    Parameters
    ----------
    file_path: str
        File path.

    Returns
    -------
    md5_hash: str
        md5 hash of data in file_path
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as fhandle:
        for chunk in iter(lambda: fhandle.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def make_index(data_path):
    
    metadata_rel_path = os.path.join("metadata", "UrbanSound8K.csv")

    index = {
        "version": "1.0",
        "clips": {},
        "metadata": {"UrbanSound8K.csv": [metadata_rel_path, md5(os.path.join(data_path, metadata_rel_path))]}
    }

    for i in range(1, 11):

        fold_dir = os.path.join(data_path, "audio", "fold{}".format(i))

        wavfiles = glob.glob(os.path.join(fold_dir, "*.wav"))

        for wf in wavfiles:

            clip_id = os.path.basename(wf).replace(".wav", "")
            index["clips"][clip_id] = \
                {"audio": [os.path.join("audio", "fold{}".format(i), os.path.basename(wf)), md5(wf)]}

    with open(INDEX_PATH, "w") as fhandle:
        json.dump(index, fhandle, indent=2)


def main(args):
    make_index(args.data_path)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Generate urbansound8k index file.")
    PARSER.add_argument("data_path", type=str, help="Path to urbansound8k data folder.")

    main(PARSER.parse_args())
