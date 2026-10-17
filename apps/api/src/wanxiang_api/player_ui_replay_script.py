"""Historical replay and chronicle controls for the Player World Stage.

Classic scripts share one global lexical environment, so this module can use the
helpers (`$`, `tr`, `safe`, `rowList`, `api`, `busy`, `status`) and the `model`
object declared by ``player_ui_script.SCRIPT`` as long as the document loads
that script first.
"""

# ruff: noqa: E501

REPLAY_SCRIPT = r"""
function renderChronicle(v,model){
  const items=model.historyExpanded&&model.history?.events?model.history.events:(v.chronicle||[]);
  $("chronicle-list").innerHTML=rowList(items,"chronicle_empty",item=>`<li><button class="chronicle-replay" type="button" data-replay-time="${Number(item.time)||0}" title="${safe(tr("replay_open"))}" aria-label="${safe(tr("replay_open"))}">${safe(tr("moment",{time:item.time}))}</button><span class="muted">${safe(item.summary)}</span></li>`);
  $("chronicle-list").querySelectorAll("[data-replay-time]").forEach(node=>node.addEventListener("click",()=>replayAt(Number(node.dataset.replayTime||0))));
  const button=$("chronicle-expand");button.hidden=!model.instanceId;button.textContent=tr(model.historyExpanded?"history_collapse":"history_expand");
}
async function toggleHistory(){
  if(!model.instanceId)return;
  if(model.historyExpanded){model.historyExpanded=false;renderPlay();return}
  busy(true);status(tr("status_loading_history"));
  try{const result=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/history?limit=200`);model.history=result;model.historyExpanded=true;renderPlay();status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function replayAt(ticks){
  if(!model.instanceId)return;
  busy(true);status(tr("status_replaying"));
  try{const result=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/replay?at_ticks=${encodeURIComponent(String(ticks))}`);model.replay=result;model.stageFocus=false;renderPlay();status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
function exitReplay(){if(!model.replay)return;model.replay=null;renderPlay()}
$("stage-replay-exit").addEventListener("click",exitReplay);
$("chronicle-expand").addEventListener("click",toggleHistory);
"""
