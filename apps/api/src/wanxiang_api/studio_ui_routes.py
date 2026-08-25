"""Small browser Studio for the shared authoring use cases."""

# The embedded browser bundle is intentionally readable as one self-contained asset.
# ruff: noqa: E501

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/studio")

_HTML = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Wanxiang Studio</title>
<style>body{font:15px system-ui;max-width:960px;margin:2rem auto;padding:0 1rem;background:#111827;color:#e5e7eb}button,input{padding:.55rem;margin:.25rem;background:#1f2937;color:inherit;border:1px solid #4b5563;border-radius:4px}textarea{width:100%;height:14rem;background:#0b1220;color:#e5e7eb;border:1px solid #4b5563;padding:.6rem}pre{white-space:pre-wrap;background:#0b1220;padding:1rem;max-height:28rem;overflow:auto}.row{display:flex;gap:.5rem;flex-wrap:wrap}.muted{color:#9ca3af}</style></head>
<body><h1>Wanxiang Studio</h1><p class="muted">Upload → Progress → Candidates/Review → Domains/Completion/Draft → Build/Preview → Worldness/Repair → Living World</p>
<div class="row"><input id="job" value="studio_job" aria-label="job id"><input id="provider" value="local" aria-label="semantic provider"></div>
<textarea id="source" aria-label="source text">Paste source text or load a file</textarea><div class="row">
<input id="file" type="file"><button onclick="runAuthoring()">Run authoring</button><button onclick="loadStatus()">Refresh status</button>
<button onclick="buildDraft()">Build</button><button onclick="previewDraft()">Preview</button><button onclick="runWorldness()">Worldness / repair</button><button onclick="enterWorld()">Enter living world</button></div>
<pre id="out">Ready.</pre>
<script>
const out=document.getElementById('out'), job=()=>document.getElementById('job').value;
async function call(path, options={}){const r=await fetch(path,options);const x=await r.json();out.textContent=JSON.stringify(x,null,2);if(!r.ok)throw x;return x}
async function loadStatus(){return call('/studio/jobs/'+encodeURIComponent(job()))}
async function buildDraft(){return call('/studio/jobs/'+encodeURIComponent(job())+'/build',{method:'POST'})}
async function previewDraft(){return call('/studio/jobs/'+encodeURIComponent(job())+'/preview',{method:'POST'})}
async function runAuthoring(){
 const file=document.getElementById('file').files[0]; const content=file?await file.text():document.getElementById('source').value;
 const body={job_id:job(),profile:'book',semantic_provider:document.getElementById('provider').value||null,sources:[{source_id:'studio_source',kind:'text',content,stage:'E3',rights_approved:true,access:'private',package_inclusion_allowed:true,private_analysis_allowed:true}]};
 const x=await call('/studio/one-click',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)});
 await call('/studio/jobs/'+encodeURIComponent(job())+'/draft'); await call('/studio/jobs/'+encodeURIComponent(job())+'/review-inbox'); return x;
}
async function runWorldness(){await call('/studio/jobs/'+encodeURIComponent(job())+'/worldness',{method:'POST'});}
async function enterWorld(){await call('/studio/jobs/'+encodeURIComponent(job())+'/enter',{method:'POST'});}
</script></body></html>"""


@router.get("/ui", response_class=HTMLResponse)
def studio_ui() -> HTMLResponse:
    return HTMLResponse(_HTML)
