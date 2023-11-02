import os
import json
import argparse
from natsort import natsorted
from util import get_logger


def get_args(description="Converts json file format"):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--input_jsons_dir",
        type=str,
        default="",
        help="Input directory of json files to be converted",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="",
        help="Output directory where the converted file and the log file will be saved",
    )
    parser.add_argument(
        "--output_json_filename", type=str, default="", help="Output json file name"
    )
    parser.add_argument(
        "--source_format",
        type=str,
        choices=["alchera", "msrvtt"],
        help="Source annotation format type",
    )
    parser.add_argument(
        "--target_format",
        type=str,
        choices=["alchera", "msrvtt"],
        help="Target annotation format type",
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

    #############################
    # Read source json files
    if args.source_format == "alchera":
        json_files = os.listdir(args.input_jsons_dir)
        json_files = natsorted(json_files)
        logger.info("Source json directory: {}".format(args.input_jsons_dir))

        data = [None] * len(json_files)
        for idx, json_file in enumerate(json_files):
            json_filepath = os.path.join(args.input_jsons_dir, json_file)

            with open(json_filepath, "r", encoding="utf-8-sig") as f:
                single_data = json.load(f)

            data[idx] = single_data

    elif args.source_format == "msrvtt":
        raise NotImplementedError
    else:
        raise NotImplementedError

    #############################
    # Convert json files
    if args.target_format == "alchera":
        raise NotImplementedError
    elif args.target_format == "msrvtt":
        video_idx = 0
        sen_idx = 0
        videos = [None] * len(data)
        sentences = [None] * len(data) * 5

        for data_i, single_data in enumerate(data):
            video_info = {
                "filename": single_data["videos"][0]["filename"],
                "duration": single_data["videos"][0]["duration"],
                "source": single_data["videos"][0]["source"],
                "person_present": single_data["videos"][0]["person_present"],
                "sub-category": single_data["videos"][0]["sub-category"],
                "activity": single_data["videos"][0]["activity"],
                "composition": single_data["videos"][0]["composition"],
                "location": single_data["videos"][0]["location"],
                "audio": single_data["videos"][0]["audio"],
                "time": single_data["videos"][0]["time"],
                "video_id": f"video{str(video_idx)}",
            }
            videos[data_i] = video_info

            num_sentences = len(single_data["videos"][0]["eng_sentences"])
            for sen_i in range(num_sentences):
                sentence_info = {
                    "kor_sentences": single_data["videos"][0]["kor_sentences"][sen_i],
                    "caption": single_data["videos"][0]["eng_sentences"][sen_i],
                    "words_per_sentence": single_data["videos"][0][
                        "words_per_sentence"
                    ][sen_i],
                    "video_id": f"video{str(video_idx)}",
                    "sen_id": sen_idx,
                }

                sentences[sen_idx] = sentence_info

                sen_idx += 1

            video_idx += 1

        converted_data = {
            "videos": videos,
            "sentences": sentences,
        }

        logger.info("Converted json keys: {}".format(converted_data.keys()))
        logger.info(
            "Converted json number of videos: {}".format(len(converted_data["videos"]))
        )
        logger.info(
            "Converted json number of sentences: {}".format(
                len(converted_data["sentences"])
            )
        )
    else:
        raise NotImplementedError

    #############################
    # Save converted json files
    output_filepath = os.path.join(args.output_dir, args.output_json_filename)
    with open(output_filepath, "w") as f:
        json.dump(converted_data, f, indent=4, ensure_ascii=False)

    logger.info("Saved converted json file: {}".format(output_filepath))

    logger.info("Done")


if __name__ == "__main__":
    main()
