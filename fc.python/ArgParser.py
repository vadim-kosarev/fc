import argparse

# ------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(
    description='processes faces image')
parser.add_argument(
    "--file",
    type=str,
    default="out/input.jpg",
    help="source file")
parser.add_argument(
    "--suffix",
    type=str,
    default="_dnn.jpeg",
    help="outfile suffix")
parser.add_argument(
    "--outdir",
    type=str,
    default="out",
    help="Output directory")
parser.add_argument(
    "--label",
    type=str,
    default="",
    help="Info label")
parser.add_argument(
    "--debug",
    type=bool,
    default=False,
    help="Dump debug images and info")

args = parser.parse_args()
