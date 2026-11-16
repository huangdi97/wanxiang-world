"""Browser controller for explicit, owner-only T2 panorama upgrades."""

# ruff: noqa: E501

PANORAMA_UPGRADE_SCRIPT = r"""
(()=>{
let state=null,profile="",apiClient=null,statePlace="";
const byId=id=>document.getElementById(id);
const reasonKey=value=>({
  provider_not_configured:"panorama_upgrade_unavailable_provider",
  provider_not_panorama:"panorama_upgrade_unavailable_provider",
  network_not_allowed:"panorama_upgrade_unavailable_network",
  source_external_processing_not_allowed:"panorama_upgrade_unavailable_rights",
  private_source_provider_not_safe:"panorama_upgrade_unavailable_privacy",
  budget_insufficient:"panorama_upgrade_unavailable_budget",
  budget_ledger_unavailable:"panorama_upgrade_unavailable_budget",
  package_not_found:"panorama_upgrade_unavailable_provider"
}[value]||"panorama_upgrade_unavailable_provider");
async function load(profileId,api){
  profile=profileId||"";state=null;statePlace="";apiClient=api||null;
  if(!profile||!apiClient)return null;
  try{state=await apiClient("/experience/player/worlds/"+encodeURIComponent(profile)+"/panoramas")}catch{state=null}
  return state
}
function paint(scene,tr){
  const panel=byId("panorama-upgrade-panel"),submit=byId("panorama-upgrade-submit"),copy=byId("panorama-upgrade-copy");
  if(!panel||!submit||!copy)return;
  const place=scene?.place_name||"",generation=state?.generation||{},ready=Boolean(place&&(scene?.presentation_kind==="panorama"||(state?.ready_places||[]).includes(place)));
  panel.hidden=!place||!state;
  if(panel.hidden){submit.hidden=true;submit.dataset.place="";return}
  copy.textContent=ready?tr("panorama_upgrade_ready",{place}):generation.resume_reserved?tr("panorama_upgrade_resume",{place}):generation.available?tr("panorama_upgrade_available",{place,cost:generation.cost_units||0,remaining:generation.budget_remaining||0,budget:generation.budget_total||0}):tr(reasonKey(generation.reason));
  submit.hidden=ready||!generation.available;submit.dataset.place=place;submit.textContent=tr(generation.resume_reserved?"panorama_upgrade_resume_submit":"panorama_upgrade_submit");
}
function render(scene,tr){
  const place=scene?.place_name||"";
  paint(scene,tr);
  if(!place||!profile||!apiClient||statePlace===place)return;
  statePlace=place;
  const requested=place;
  void apiClient("/experience/player/worlds/"+encodeURIComponent(profile)+"/panoramas?place_name="+encodeURIComponent(place)).then(next=>{if(statePlace===requested){state=next;paint(scene,tr)}}).catch(()=>{});
}
window.__WANXIANG_PANORAMA_UPGRADE__={load,render,profile:()=>profile};
})();
"""
