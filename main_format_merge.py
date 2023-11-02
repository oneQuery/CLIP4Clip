import os
import argparse
import json
from itertools import chain
from util import get_logger
import datetime
from tqdm import tqdm


def get_args(description="Merge json files"):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--input_json_filepaths",
        nargs="*",
        type=str,
        default="",
        help="Input json file paths to be merged",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="",
        help="Output directory",
    )
    parser.add_argument(
        "--output_json_filename",
        type=str,
        default="",
        help="Output json file name",
    )
    parser.add_argument(
        "--format_type",
        type=str,
        choices=["msrvtt"],
        default="",
        help="Format type of the input json files",
    )
    return parser.parse_args()


def set_logger(args):
    global logger

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    logger = get_logger(filename=os.path.join(args.output_dir, "log.txt"))

    logger.info("Effective parameters:")
    for key in sorted(args.__dict__):
        logger.info("  <<< {}: {}".format(key, args.__dict__[key]))


def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def write_json(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    logger.info(f"Write merged json file: {file_path}")


def reassign_ids(videos, sentences, video_id_offset, sen_id_offset):
    new_videos = []
    new_sentences = []
    video_id_map = {}

    for i, video in enumerate(videos):
        new_video_id = f"video{video_id_offset + i}"
        video_id_map[video["video_id"]] = new_video_id
        video["video_id"] = new_video_id
        new_videos.append(video)

    for sen in sentences:
        old_video_id = sen["video_id"]
        sen["video_id"] = video_id_map.get(old_video_id, old_video_id)
        sen["sen_id"] = sen_id_offset
        sen_id_offset += 1
        new_sentences.append(sen)

    return new_videos, new_sentences, video_id_offset + len(videos), sen_id_offset


def main():
    global logger
    args = get_args()
    set_logger(args)

    merged_videos = []
    merged_sentences = []
    video_id_offset = 0
    sen_id_offset = 0

    for json_path in args.input_json_filepaths:
        data = read_json(json_path)
        videos, sentences, video_id_offset, sen_id_offset = reassign_ids(
            data["videos"], data["sentences"], video_id_offset, sen_id_offset
        )
        merged_videos.extend(videos)
        merged_sentences.extend(sentences)

    merged_data = {"videos": merged_videos, "sentences": merged_sentences}

    output_json_filepath = os.path.join(args.output_dir, args.output_json_filename)
    write_json(merged_data, output_json_filepath)


if __name__ == "__main__":
    main()
