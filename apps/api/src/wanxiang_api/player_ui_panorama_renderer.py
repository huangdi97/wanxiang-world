"""Renderer-neutral browser bridge for T2 panorama projections."""

# ruff: noqa: E501

PANORAMA_RENDERER_SCRIPT = r"""
(()=>{
const state={active:false,key:"",scene:null,cleanup:null};
const byId=id=>document.getElementById(id);
const renderer=()=>window.__WANXIANG_PANORAMA_RENDERER__||null;
const canRender=scene=>{try{const r=renderer();return Boolean(scene?.presentation_kind==="panorama"&&scene?.data_uri&&r&&typeof r.mount==="function"&&(!r.supports||r.supports(scene.media_type||"")))}catch{return false}};
const setButton=(available,active)=>{const button=byId("panorama-stage-toggle");if(!button)return;button.hidden=!available;button.setAttribute("aria-pressed",String(Boolean(active)))};
async function deactivate(){
  const host=byId("world-stage-panorama"),r=renderer();
  try{if(typeof state.cleanup==="function")await state.cleanup();else if(r&&typeof r.unmount==="function"&&host)await r.unmount(host)}catch{}finally{
    state.cleanup=null;state.active=false;if(host){host.replaceChildren();host.hidden=true}setButton(canRender(state.scene),false)
  }
  return false
}
async function activate(){
  const host=byId("world-stage-panorama"),r=renderer(),scene=state.scene;
  if(!host||!r||!canRender(scene))return false;
  await window.__WANXIANG_SPATIAL_STAGE__?.deactivate();
  host.hidden=false;host.replaceChildren();
  try{
    const cleanup=await r.mount({container:host,placeName:scene.place_name||"",dataUri:scene.data_uri,mediaType:scene.media_type||""});
    state.cleanup=typeof cleanup==="function"?cleanup:null;state.active=true;setButton(true,true);return true
  }catch(error){await deactivate();throw error}
}
function sync(scene){
  const key=`${scene?.place_name||""}:${scene?.content_sha256||""}:${scene?.presentation_kind||""}`,changed=key!==state.key,wasActive=state.active;
  state.key=key;state.scene=scene||null;
  const available=canRender(state.scene);setButton(available,state.active);
  if(!available&&state.active){void deactivate();return}
  if(changed&&wasActive){void deactivate().then(()=>activate()).catch(()=>{})}
}
window.__WANXIANG_PANORAMA_STAGE__={sync,toggle:async()=>state.active?deactivate():activate(),deactivate,isActive:()=>state.active};
})();
"""
