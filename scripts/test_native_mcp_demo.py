#!/usr/bin/env python3
"""Authorized scratch-only native MCP move/undo smoke test. Never saves a font."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import selectors
import uuid

ROOT = Path(__file__).resolve().parents[1]


def run(binary, scratch, output):
    scratch = Path(scratch).resolve()
    allowed = (ROOT / 'out/native-mcp-demo').resolve()
    if not scratch.is_relative_to(allowed) or scratch.suffix != '.ufo':
        raise ValueError('Only a UFO inside out/native-mcp-demo is allowed')
    before_disk = {str(p.relative_to(scratch)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in scratch.rglob('*') if p.is_file()}
    proc = subprocess.Popen([binary, 'mcp', '--live'], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, text=True)
    serial = 0

    def call(name, arguments=None, allow_error=False):
        nonlocal serial
        serial += 1
        proc.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': serial, 'method': 'tools/call',
                                    'params': {'name': name, 'arguments': arguments or {}}}) + '\n')
        proc.stdin.flush()
        with selectors.DefaultSelector() as ready:
            ready.register(proc.stdout, selectors.EVENT_READ)
            if not ready.select(timeout=35):
                raise TimeoutError('MCP reply timeout; inspect operation receipt before retrying')
        result = json.loads(proc.stdout.readline())['result']
        value = result.get('structuredContent')
        if value is None:
            value = json.loads(result['content'][0]['text'])
        if not allow_error and not value.get('ok', False):
            raise RuntimeError(value)
        return value

    applied = False
    identity = None
    receipt = {}
    try:
        for session in call('editor_sessions')['sessions']:
            project = call('editor_connect', {'session': session}, allow_error=True)
            if project.get('ok') and project.get('project') and Path(project['project']).resolve() == scratch:
                break
        else:
            raise RuntimeError('Exact scratch window not open; no edit attempted')
        call('design_context')
        call('editor_open_glyph', {'glyph': 'lam-ar'})
        r = call('read_glyph', {'glyph': 'lam-ar', 'source': project['active_source']})
        point = next(p for c in r['contours'] for p in c if p['type'] == 'offcurve')
        guard = {'glyph': r['glyph'], 'glyph_id': r['glyph_id'], 'layer': r['layer'],
                 'expected_revision': r['revision']}
        identity = {'expected_document_epoch': r['document_epoch'], 'actor': 'codex-demo-test',
                    'operation_key': 'scratch-' + uuid.uuid4().hex}
        payload = {**identity, 'authorization': 'user-approved', 'source': r['source_id'],
                   'history_name': 'Scratch MCP point test', 'edits': [{'target': guard,
                   'operations': [{'op': 'set_point', 'point_id': point['id'],
                                   'x': point['x'] + 32, 'y': point['y']}]}]}
        receipt['before'] = r
        receipt['apply'] = call('agent_apply', payload)
        applied = True
        changed = call('read_glyph', {'glyph': 'lam-ar', 'source': r['source_id']})
        expected = json.loads(json.dumps(r['contours']))
        for contour in expected:
            for p in contour:
                if p['id'] == point['id']:
                    p['x'] += 32
        assert changed['contours'] == expected, 'Unexpected point changes'
        receipt['duplicate_apply'] = call('agent_apply', payload)
        duplicate = call('read_glyph', {'glyph': 'lam-ar', 'source': r['source_id']})
        assert duplicate['contours'] == expected, 'Retry changed geometry'
        # A different operation using the stale read must reject.
        stale = dict(payload, operation_key='stale-' + uuid.uuid4().hex)
        receipt['stale_rejection'] = call('agent_apply', stale, allow_error=True)
        assert receipt['stale_rejection'].get('ok') is False
        receipt['undo'] = call('agent_history', {**identity, 'direction': 'undo',
                                               'authorization': 'user-approved'})
        applied = False
        restored = call('read_glyph', {'glyph': 'lam-ar', 'source': r['source_id']})
        for key in ('contours', 'anchors', 'advance', 'components', 'component_transforms'):
            assert restored[key] == r[key], key
        after_disk = {str(p.relative_to(scratch)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in scratch.rglob('*') if p.is_file()}
        assert after_disk == before_disk, 'Unexpected disk write'
        receipt.update(restored_geometry=True, disk_unchanged=True, saved=False,
                       model_used=False, project=str(scratch))
        Path(output).write_text(json.dumps(receipt, indent=2) + '\n')
        print('PASS: native point move, idempotent retry, stale-read rejection, undo, disk unchanged')
    finally:
        if applied and identity:
            print('Attempting rollback after failed verification')
            print(call('agent_history', {**identity, 'direction': 'undo',
                                        'authorization': 'user-approved'}, allow_error=True))
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--binary', required=True)
    p.add_argument('--scratch', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    run(a.binary, a.scratch, a.output)
