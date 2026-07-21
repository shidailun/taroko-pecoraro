"""Upload Truku TTS mp3 clips to the Cloudflare R2 bucket `taroko-audio`.

Clips are named `<item-id>.mp3` (the id from tts_full/items.json) and uploaded
under the same flat key, so the app plays  R2_PUBLIC_URL + "/" + id + ".mp3".

Reads credentials from tools/.env.r2 (gitignored). Idempotent: skips objects
already present with the same size unless --force. Content is immutable, so we
set a one-year immutable Cache-Control.

Usage:
    python tools/upload_audio_r2.py --test     # upload one file, then stop
    python tools/upload_audio_r2.py            # upload all (skip already-present)
    python tools/upload_audio_r2.py --force    # re-upload everything
"""
import argparse
import concurrent.futures as cf
import threading
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = Path(r"C:\dev\formosan\ilrdf\tts_truku_mp3")
ENV = ROOT / "tools" / ".env.r2"
CACHE = "public, max-age=31536000, immutable"


def load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="upload only the first file")
    ap.add_argument("--force", action="store_true", help="re-upload even if present")
    ap.add_argument("--dir", default=str(AUDIO_DIR), help="mp3 source dir (default: %(default)s)")
    ap.add_argument("--workers", type=int, default=24)
    args = ap.parse_args()
    audio_dir = Path(args.dir)

    env = load_env(ENV)
    bucket = env["R2_BUCKET"]
    session = boto3.session.Session()
    cfg = Config(signature_version="s3v4", retries={"max_attempts": 5, "mode": "standard"},
                 max_pool_connections=args.workers + 4)

    def client():
        return session.client(
            "s3", endpoint_url=env["R2_ENDPOINT"],
            aws_access_key_id=env["R2_ACCESS_KEY_ID"],
            aws_secret_access_key=env["R2_SECRET_ACCESS_KEY"],
            config=cfg, region_name="auto")

    files = sorted(audio_dir.glob("*.mp3"))
    if args.test:
        files = files[:1]
    total = len(files)

    local = threading.local()
    counts = {"up": 0, "skip": 0, "err": 0}
    lock = threading.Lock()

    def worker(fp):
        s3 = getattr(local, "s3", None)
        if s3 is None:
            s3 = local.s3 = client()
        key = fp.name
        size = fp.stat().st_size
        if not args.force:
            try:
                if s3.head_object(Bucket=bucket, Key=key)["ContentLength"] == size:
                    with lock:
                        counts["skip"] += 1
                    return
            except ClientError as e:
                if e.response["Error"]["Code"] not in ("404", "NoSuchKey", "403"):
                    raise
        s3.upload_file(str(fp), bucket, key,
                       ExtraArgs={"ContentType": "audio/mpeg", "CacheControl": CACHE})
        with lock:
            counts["up"] += 1

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(worker, fp): fp for fp in files}
        done = 0
        for fut in cf.as_completed(futs):
            done += 1
            try:
                fut.result()
            except Exception as e:
                with lock:
                    counts["err"] += 1
                print(f"ERR {futs[fut].name}: {e}")
            if done % 500 == 0 or done == total:
                print(f"[{done}/{total}] up={counts['up']} skip={counts['skip']} err={counts['err']}")

    print(f"\nDone. uploaded={counts['up']} skipped={counts['skip']} errors={counts['err']} total={total}")
    if args.test and counts["up"]:
        print("Test upload OK — token can write to this bucket.")


if __name__ == "__main__":
    main()
