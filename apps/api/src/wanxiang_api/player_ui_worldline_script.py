"""Worldline fork and switching controls for the Player World Stage.

A fork creates a real Kernel child branch and a detached Player handle; the list
shows every playable worldline of the runtime instance and lets the player
switch by leaving the current session and continuing the chosen handle.
"""

# ruff: noqa: E501

WORLDLINE_SCRIPT = r"""
function worldlineCard(card,index){
  const current=Boolean(card.current),meta=[tr("worldline_time",{time:card.world_time})];
  if(card.forked_from_revision!==null&&card.forked_from_revision!==undefined)meta.push(tr("worldline_forked_at",{revision:card.forked_from_revision}));
  return `<li data-worldline="${safe(card.instance_id)}" data-current="${current?"true":"false"}"><div class="worldline-copy"><strong>${safe(tr("worldline_label",{index:index+1}))}${current?` <span class="worldline-badge">${safe(tr("worldline_current"))}</span>`:""}</strong><span class="muted">${safe(meta.join(" · "))}</span></div>${current?"":`<button class="secondary-button" type="button" data-switch-worldline="${safe(card.instance_id)}">${safe(tr("worldline_switch"))}</button>`}</li>`;
}
function renderWorldlines(cards){
  const list=$("worldline-list");
  list.innerHTML=cards.length?cards.map(worldlineCard).join(""):`<li class="muted">${safe(tr("worldlines_empty"))}</li>`;
  list.querySelectorAll("[data-switch-worldline]").forEach(node=>node.addEventListener("click",()=>switchWorldline(node.dataset.switchWorldline||"")));
}
async function toggleWorldlines(){
  const panel=$("worldline-panel");
  if(!panel.hidden){panel.hidden=true;return}
  if(!model.instanceId)return;
  busy(true);
  try{const data=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/worldlines`);renderWorldlines(data.worldlines||[]);panel.hidden=false}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function switchWorldline(handle){
  if(!handle||handle===model.instanceId)return;
  busy(true);status(tr("status_switching_worldline"));
  try{
    if(model.instanceId)await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/leave`,{method:"POST"}).catch(()=>{});
    const result=await api(`/experience/player/instances/${encodeURIComponent(handle)}/continue`,{method:"POST"});
    model.instanceId=result.instance_id;model.view=result.view;model.replay=null;model.history=null;model.historyExpanded=false;model.observerScene="";model.stageFocus=false;
    $("worldline-panel").hidden=true;renderPlay();status(tr("status_worldline_switched"));
  }catch(error){status(error.message,true)}finally{busy(false)}
}
async function forkWorldline(){
  if(!model.instanceId)return;
  const parent=model.instanceId;busy(true);status(tr("status_forking"));
  try{
    const result=await api(`/experience/player/instances/${encodeURIComponent(parent)}/fork`,{method:"POST"});
    await api(`/experience/player/instances/${encodeURIComponent(parent)}/leave`,{method:"POST"}).catch(()=>{});
    window.__WANXIANG_LAST_FORKED_WORLDLINE__=result.worldline;
    model.instanceId="";model.view=null;model.replay=null;model.history=null;model.historyExpanded=false;model.observerScene="";model.stageFocus=false;
    view("home-view");await loadHome();status(tr("status_forked"));
  }catch(error){status(error.message,true)}finally{busy(false)}
}
$("fork-worldline").addEventListener("click",forkWorldline);
$("worldline-toggle").addEventListener("click",toggleWorldlines);
$("worldline-close").addEventListener("click",()=>{$("worldline-panel").hidden=true});
"""
