from pathlib import Path
import json
import shutil
import subprocess
import sys

root = Path('/home/ubuntu/rollout/ripple')
out = Path('/home/ubuntu/accept-kit/audit/ripple/smoke')
out.mkdir(parents=True, exist_ok=True)

def run(args, expected=0):
    result = subprocess.run(args, cwd=out, text=True, capture_output=True)
    (out / 'commands.log').open('a').write('$ ' + ' '.join(map(str, args)) + '\n' + result.stdout + result.stderr + f'\nexit {result.returncode}\n')
    assert result.returncode == expected, (args, result.stdout[-2000:], result.stderr[-2000:])
    return result

sources = list(root.glob('*.py')) + list((root/'scripts').glob('*.py'))
for path in sources:
    compile(path.read_text(), str(path), 'exec')
print(f'PASS: syntax compile of {len(sources)} tracked Python files (in memory)')
for name in ['pipeline', 'combine', 'cut', 'recap']:
    run([sys.executable, str(root / f'inkling-video-{name}.py'), '--help'])
print('PASS: four argparse CLI help commands')
run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=size=320x180:rate=10', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=44100', '-t', '6', '-c:v', 'libx264', '-c:a', 'aac', str(out/'source.mp4')])
(out/'transcript.srt').write_text('1\n00:00:00,000 --> 00:00:01,000\nSynthetic smoke fixture, not event footage.\n')
shutil.copyfile(root/'inkling-demo-master-prompt.txt', out/'inkling-demo-master-prompt.txt')
run([sys.executable, str(root/'inkling-video-pipeline.py'), '--video', str(out/'source.mp4'), '--transcript', str(out/'transcript.srt')])
frames = list((out/'frames').glob('*.jpg'))
assert frames and all(p.stat().st_size < 2097152 for p in frames)
assert 'Synthetic smoke fixture' in (out/'inkling-video-playground-pack.txt').read_text()
print(f'PASS: supplied-transcript pipeline produced pack and {len(frames)} keyframe(s) below 2 MB on synthetic footage')
picks=out/'picks.jsonl'
picks.write_text(json.dumps({'clip': {'start': '0:00', 'end': '0:01', 'title': 'synthetic smoke'}})+'\n')
run([sys.executable, str(root/'inkling-video-cut.py'), '--video', str(out/'source.mp4'), '--picks', str(picks), '--out', str(out/'clips')])
run([sys.executable, str(root/'inkling-video-recap.py'), '--video', str(out/'source.mp4'), '--picks', str(picks), '--out', str(out/'recap.mp4')])
assert list((out/'clips').glob('*.mp4'))
probe=run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(out/'recap.mp4')])
assert 0.8 < float(probe.stdout) < 1.5
print('PASS: actual ffmpeg clip + recap; output duration between 0.8 and 1.5 seconds (synthetic fixture only)')
missing=run([sys.executable, str(root/'inkling-video-pipeline.py'), '--video', str(out/'missing.mp4')], expected=1)
assert 'Video not found' in missing.stdout
print('PASS: missing input reports Video not found and exits 1')
messages=[{'jsonrpc':'2.0','id':1,'method':'initialize'}, {'jsonrpc':'2.0','id':2,'method':'tools/list'}, {'jsonrpc':'2.0','id':3,'method':'ping'}]
mcp=subprocess.run([sys.executable,str(root/'inkling-video-editor-mcp.py')], input=''.join(json.dumps(m)+'\n' for m in messages), text=True,capture_output=True,cwd=out)
responses=[json.loads(line) for line in mcp.stdout.splitlines()]
assert mcp.returncode==0 and len(responses)==3 and len(responses[1]['result']['tools'])==5
print('PASS: MCP initialize, tools/list (5 tools), ping')
print('NOT RUN: Whisper transcription, Tinker picking/training, or original event reconstruction; source artifacts/access unavailable')
