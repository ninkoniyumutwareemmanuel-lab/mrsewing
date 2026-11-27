#!/usr/bin/env python3
"""Prepare/check SILENT derivatives of the registered homepage videos.

Original MP4 files stay unchanged. Temporary derivatives are deleted at end
of a normal check; nothing is emitted into deployed website assets or pages.
Use --output-dir for controlled preparation outside the public repo; the build
workflow explicitly copies verified outputs into approved publication paths.
Preparation does not grant or change rights, poster or publication approval.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(path):
    output=subprocess.run([
        shutil.which('ffprobe') or 'ffprobe', '-v', 'error', '-show_streams',
        '-show_format', '-of', 'json', str(path)
    ], check=True, capture_output=True, text=True)
    return json.loads(output.stdout)


def prepare(destination):
    videos=json.loads((ROOT/'_data/media-video-records.json').read_text())['videos']
    if len(videos)!=2:
        raise ValueError('Expected exactly two R53 reviewed video sources')
    ffmpeg=shutil.which('ffmpeg')
    if not ffmpeg or not shutil.which('ffprobe'):
        raise RuntimeError('FFmpeg and ffprobe required for verified silent video preparation')
    destination.mkdir(parents=True, exist_ok=True)
    outcomes=[]
    for video in videos:
        filename=Path(video['assetPath']).name
        original=ROOT/filename
        if not original.is_file() or sha256(original)!=video['technicalReview']['sha256']:
            raise ValueError('Original video missing or not the reviewed R53 bytes: '+filename)
        prior=sha256(original)
        output=destination/(original.stem+'-silent.mp4')
        command=[ffmpeg,'-hide_banner','-loglevel','error','-nostdin','-y',
                 '-i',str(original),'-map','0:v:0','-c:v','copy','-an',
                 '-movflags','+faststart',str(output)]
        subprocess.run(command,check=True,capture_output=True,text=True)
        streams=inspect(output)['streams']
        video_streams=[s for s in streams if s.get('codec_type')=='video']
        audio_streams=[s for s in streams if s.get('codec_type')=='audio']
        if len(video_streams)!=1 or audio_streams:
            raise ValueError('Silent derivative validation failed for '+filename)
        if sha256(original)!=prior:
            raise ValueError('Original video unexpectedly modified: '+filename)
        outcomes.append({
            'original':filename,'originalSha256':prior,'silentSha256':sha256(output),
            'audioStreams':0,'videoStreams':1,'publicationStatus':video.get('publicationStatus'),
            'preparationChangesApproval':False
        })
    return outcomes


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',help='Controlled, non-public output directory (otherwise temporary)')
    args=parser.parse_args()
    if args.output_dir:
        target=Path(args.output_dir).resolve()
        if target.is_relative_to(ROOT):
            raise SystemExit('Use an external preparation directory; publication copies belong to the reviewed build workflow')
        result=prepare(target)
    else:
        with tempfile.TemporaryDirectory(prefix='mrsewing-r56-silent-') as folder:
            result=prepare(Path(folder))
    print(json.dumps(result,indent=2))
    print('PASS: Both temporary playback copies contain no audio; original files and publication approvals remain unchanged')
