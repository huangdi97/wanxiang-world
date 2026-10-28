"""Worldline fork, list, switch, and comparison controls for the Player Stage.

Forks create real Kernel child branches as detached Player handles; the panel
lists every playable worldline, lets the player compare two heads through a
read-only endpoint, and switches by leaving the current session and continuing
the chosen handle.
"""

# ruff: noqa: E501

WORLDLINE_SCRIPT = r"""
function worldlineCard(card,index){
  const current=Boolean(card.current),meta=[tr("worldline_time",{time:card.world_time})];
  if(card.forked)meta.push(tr("worldline_forked"));
  const actions=current?"":`<div class="worldline-actions"><button class="secondary-button" type="button" data-compare-worldline="${safe(card.instance_id)}">${safe(tr("worldline_compare"))}</button><button class="secondary-button" type="button" data-switch-worldline="${safe(card.instance_id)}">${safe(tr("worldline_switch"))}</button></div>`;
  return `<li data-worldline="${safe(card.instance_id)}" data-current="${current?"true":"false"}"><div class="worldline-copy"><strong>${safe(tr("worldline_label",{index:index+1}))}${current?` <span class="worldline-badge">${safe(tr("worldline_current"))}</span>`:""}</strong><span class="muted">${safe(meta.join(" · "))}</span></div>${actions}</li>`;
}
function worldlineSide(label,row,count){
  const people=(row.present_people||[]).join("、");
  return `<div class="worldline-side"><span class="stage-label">${safe(label)}</span><strong>${safe(tr("worldline_time",{time:row.world_time}))}</strong><span class="muted">${safe(shown(row.location))} · ${safe(shown(row.status))}</span><span class="muted">${safe(tr("worldline_compare_events",{count:count||0}))}${people?` · ${safe(people)}`:""}</span></div>`;
}
function worldlineRecent(label,rows){
  return `<div class="worldline-recent"><span class="stage-label">${safe(label)}</span><ul class="plain-list">${rows.length?rows.map(row=>`<li><span class="muted">${safe(tr("moment",{time:row.time}))}</span> ${safe(row.summary)}</li>`).join(""):`<li class="muted">${safe(tr("chronicle_empty"))}</li>`}</ul></div>`;
}
function renderWorldlineCompare(data){
  const block=$("worldline-compare"),left=data.left||{},right=data.right||{},diverged=data.diverged_events||{};
  const differences=data.differences||{},items=differences.items||[];
  const recent=data.recent||{},recentHtml=`<div class="worldline-recent-block"><strong>${safe(tr("worldline_recent"))}</strong><div class="worldline-recent-grid">${worldlineRecent(tr("worldline_compare_this"),recent.left||[])}${worldlineRecent(tr("worldline_compare_other"),recent.right||[])}</div></div>`;
  const diffHtml=`<div class="worldline-diff"><strong>${safe(tr("worldline_compare_diff",{count:differences.total??0}))}</strong><ul class="plain-list">${items.length?items.slice(0,5).map(item=>`<li>${safe(item.name)} <span class="muted">${safe(item.category)}</span></li>`).join(""):`<li class="muted">${safe(tr("worldline_compare_no_diff"))}</li>`}</ul></div>`;
  block.innerHTML=`<div class="worldline-compare-head"><strong>${safe(tr("worldline_compare_heading"))}</strong><span class="muted">${safe(tr("worldline_compare_common"))}</span></div><div class="worldline-compare-grid">${worldlineSide(tr("worldline_compare_this"),left,diverged.left)}${worldlineSide(tr("worldline_compare_other"),right,diverged.right)}</div><div class="worldline-compare-badge" data-identical="${data.identical?"true":"false"}">${safe(tr(data.identical?"worldline_compare_same":"worldline_compare_diverged"))}</div>${diffHtml}${recentHtml}`;
  block.hidden=false;
}
async function compareWorldline(handle){
  if(!handle||!model.instanceId)return;
  busy(true);
  try{const data=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/compare?with=${encodeURIComponent(handle)}`);renderWorldlineCompare(data)}
  catch(error){status(error.message,true)}finally{busy(false)}
}
function renderWorldlines(cards){
  const list=$("worldline-list");
  list.innerHTML=cards.length?cards.map(worldlineCard).join(""):`<li class="muted">${safe(tr("worldlines_empty"))}</li>`;
  list.querySelectorAll("[data-compare-worldline]").forEach(node=>node.addEventListener("click",()=>compareWorldline(node.dataset.compareWorldline||"")));
  list.querySelectorAll("[data-switch-worldline]").forEach(node=>node.addEventListener("click",()=>switchWorldline(node.dataset.switchWorldline||"")));
  const compare=$("worldline-compare");compare.hidden=true;compare.innerHTML="";
}
async function toggleWorldlines(){
  const panel=$("worldline-panel");
  if(!panel.hidden){panel.hidden=true;$("worldline-toggle").focus();return}
  if(!model.instanceId)return;
  busy(true);
  try{const data=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/worldlines`);renderWorldlines(data.worldlines||[]);panel.hidden=false;$("worldline-close").focus()}
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
$("worldline-close").addEventListener("click",()=>{$("worldline-panel").hidden=true;$("worldline-toggle").focus()});
document.addEventListener("keydown",event=>{
  if(event.key!=="Escape"||$("worldline-panel").hidden)return;
  $("worldline-panel").hidden=true;
  $("worldline-toggle").focus();
});
"""
