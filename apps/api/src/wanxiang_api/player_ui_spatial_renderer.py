"""Renderer-neutral browser bridge for verified T3 Player assets."""

# ruff: noqa: E501

SPATIAL_RENDERER_SCRIPT = r"""
(()=>{
const state={active:false,key:"",scene:null,profile:"",headers:{},cleanup:null};
const byId=id=>document.getElementById(id);
const renderer=()=>window.__WANXIANG_SPATIAL_RENDERER__||null;
const canRender=scene=>{try{const r=renderer(),types=scene?.spatial?.media_types||[];return Boolean(scene?.spatial?.ready&&Number(scene.spatial.asset_count||0)>0&&r&&typeof r.mount==="function"&&(!r.supports||r.supports(types)))}catch{return false}};
const setButton=(available,active)=>{const button=byId("spatial-stage-toggle");if(!button)return;button.hidden=!available;button.setAttribute("aria-pressed",String(Boolean(active)))};
async function deactivate(){
  const host=byId("world-stage-spatial"),r=renderer();
  try{if(typeof state.cleanup==="function")await state.cleanup();else if(r&&typeof r.unmount==="function"&&host)await r.unmount(host)}catch{}finally{
    state.cleanup=null;state.active=false;if(host){host.replaceChildren();host.hidden=true}setButton(canRender(state.scene),false)
  }
  return false
}
async function activate(){
  const host=byId("world-stage-spatial"),r=renderer(),scene=state.scene;
  if(!host||!r||!canRender(scene))return false;
  await window.__WANXIANG_PANORAMA_STAGE__?.deactivate();
  const assetCount=Number(scene.spatial.asset_count||0);
  const loadAsset=async index=>{
    if(!Number.isInteger(index)||index<0||index>=assetCount)throw new RangeError("spatial asset index out of range");
    const url=`/experience/player/worlds/${encodeURIComponent(state.profile)}/spatial-assets/${index}?place_name=${encodeURIComponent(scene.place_name||"")}`;
    const response=await fetch(url,{headers:state.headers});
    if(!response.ok)throw new Error("spatial asset unavailable");
    return {blob:await response.blob(),mediaType:response.headers.get("content-type")||""};
  };
  host.hidden=false;host.replaceChildren();
  try{
    const cleanup=await r.mount({container:host,placeName:scene.place_name||"",mediaTypes:[...(scene.spatial.media_types||[])],assetCount,projectionFrame:scene.spatial.projection_frame||null,loadAsset});
    state.cleanup=typeof cleanup==="function"?cleanup:null;state.active=true;setButton(true,true);return true
  }catch(error){await deactivate();throw error}
}
function sync(scene,profile,headers){
  const frameKey=JSON.stringify(scene?.spatial?.projection_frame||null),assetRevision=scene?.spatial?.asset_revision||"",key=`${profile||""}:${scene?.place_name||""}:${assetRevision}:${scene?.spatial?.asset_count||0}:${(scene?.spatial?.media_types||[]).join(",")}:${frameKey}`,changed=key!==state.key,wasActive=state.active;
  state.key=key;state.scene=scene||null;state.profile=profile||"";state.headers=headers||{};
  const available=canRender(state.scene);setButton(available,state.active);
  if(!available&&state.active){void deactivate();return}
  if(changed&&wasActive){void deactivate().then(()=>activate()).catch(()=>{})}
}
window.__WANXIANG_SPATIAL_STAGE__={sync,toggle:async()=>state.active?deactivate():activate(),deactivate,isActive:()=>state.active};
})();
"""
