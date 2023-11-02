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


def main():
    global logger
    args = get_args()
    set_logger(args)

    ##############################
    # Read source json files
    json_filepaths = args.input_json_filepaths
    data = [None] * len(json_filepaths)
    for idx, json_filepath in enumerate(json_filepaths):
        with open(json_filepath, "r", encoding="utf-8-sig") as f:
            single_data = json.load(f)
        data[idx] = single_data
    logger.info(f"Number of json files to merge: {len(json_filepaths)}")

    ##############################
    # Assign video id and sentence id
    if args.format_type == "msrvtt":
        idx = 0
        # TODO: time optimization
        for single_data in data:
            for video in tqdm(single_data["videos"]):
                video["sen_id"] = []
                for sentence in single_data["sentences"]:
                    if video["video_id"] == sentence["video_id"]:
                        video["sen_id"].append(sentence["sen_id"])

        # TODO: Reassign video id and sentence id
        video_id_used = []
        for single_data in data:
            for video in single_data["video"]:
                if video["video_id"] not in video_id_used:
                    video_id_used.append(video["video_id"])
                elif video["video_id"] in video_id_used:
                    # TODO: Reassign video id
                    # video['video_id'] =
                    pass

    else:
        raise NotImplementedError

    ##############################
    # Merge json files
    if args.format_type == "msrvtt":
        # Get number of videos and sentences
        num_json_files = len(json_filepaths)

        videos = [None] * num_json_files
        sentences = [None] * num_json_files

        # Merge videos and sentences
        for idx, single_data in enumerate(data):
            videos[idx] = single_data["videos"]
            sentences[idx] = single_data["sentences"]

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        info = {"contributor": "PIA Space", "data_created": f"{now}"}
        merged_videos = list(chain(*videos))
        merged_sentences = list(chain(*sentences))

        merged_json = {
            "info": info,
            "videos": merged_videos,
            "sentences": merged_sentences,
        }
        logger.info(f"Number of videos: {len(merged_videos)}")
        logger.info(f"Number of sentences: {len(merged_sentences)}")

    else:
        raise NotImplementedError

    ##############################
    # Write merged json file
    output_json_filepath = os.path.join(args.output_dir, args.output_json_filename)
    with open(output_json_filepath, "w") as f:
        json.dump(merged_json, f, indent=4, ensure_ascii=False)
    logger.info(f"Write merged json file: {output_json_filepath}")


if __name__ == "__main__":
    main()
