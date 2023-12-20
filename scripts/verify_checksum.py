# Source - https://gist.githubusercontent.com/jenskr/5020d044cb8b3e2d22affa2d5e09eccf/raw/08a52dbd4f6d6552001afbaa9b8417ae73405857/checksum.py
import hashlib
import argparse
import io
import sys

parser = argparse.ArgumentParser()
parser.add_argument("file", help="File for which you want to create a hash")
parser.add_argument(
    "hashvalue", help="hash value that is determined to match the calculated hash of the file")
parser.add_argument(
    "algorithm", help="Hashing algorithm. Either md5, sha256 or sha512")
args = parser.parse_args()

file = args.file
hashval = args.hashvalue
algo = None

if args.algorithm == "sha256":
    algo = hashlib.sha256()
elif args.algorithm == "sha512":
    algo = hashlib.sha512()
elif args.algorithm == "md5":
    algo = hashlib.md5()
else:
    sys.exit("Please specify a valid hashing algorithm (Either md5, sha256 or sha512)")

with open(file, "rb") as f:
    for byte_block in iter(lambda: f.read(io.DEFAULT_BUFFER_SIZE), b""):
        algo.update(byte_block)
    digest = algo.hexdigest().upper()
print(f"Calculated hash: {digest}")

print("Hash values match. File OK!") if digest == hashval else print(
    "Hash values do not match. Data may be corrupted!")
