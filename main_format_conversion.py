import os
import argparse
from util import get_logger


def get_args(description="Converts json file format"):
    parser = argparse.ArgumentParser(description=description)
    # TODO: Add input arguments
    parser.add_argument(
        "--input_filepath", type=str, default="", help="Input file path to be converted"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="",
        help="Output directory where the converted file and the log file will be saved",
    )
    parser.add_argument(
        "--source_format",
        type="str",
        choices=["alchera", "msrvtt"],
        help="Source annotation format type",
    )
    parser.add_argument(
        "--target_format",
        type="str",
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

    print("breakpoint")


if __name__ == "__main__":
    main()
