"""Historical replay and chronicle controls for the Player World Stage.

Classic scripts share one global lexical environment, so this module can use the
helpers (`$`, `tr`, `safe`, `rowList`, `api`, `busy`, `status`) and the `model`
object declared by ``player_ui_script.SCRIPT`` as long as the document loads
that script first.
"""

# ruff: noqa: E501

REPLAY_SCRIPT = r"""
const HISTORY_PAGE_SIZE=50;
function renderChronicle(v,model){
  const expanded=!model.replay&&Boolean(model.historyExpanded&&model.history?.events);
  const items=expanded?model.history.events:(v.chronicle||[]);
  const total=Number(model.history?.total||0),returned=Number(model.history?.returned||items.length);
  const window=expanded&&total>returned?`<li class="muted chronicle-window">${safe(tr("history_window",{returned,total}))}</li>`:"";
  $("chronicle-list").innerHTML=rowList(items,"chronicle_empty",item=>`<li><button class="chronicle-replay" type="button" data-replay-time="${Number(item.time)||0}" title="${safe(tr("replay_open"))}" aria-label="${safe(tr("replay_open"))}">${safe(tr("moment",{time:item.time}))}</button><span class="muted">${safe(item.summary)}</span></li>`)+window;
  $("chronicle-list").querySelectorAll("[data-replay-time]").forEach(node=>node.addEventListener("click",()=>replayAt(Number(node.dataset.replayTime||0))));
  const button=$("chronicle-expand");button.hidden=!model.instanceId||Boolean(model.replay);button.textContent=tr(model.historyExpanded?"history_collapse":"history_expand");
  $("chronicle-more").hidden=!expanded||!model.history?.has_more;
}
async function loadMoreHistory(){
  if(!model.instanceId||!model.history?.next_before)return;
  busy(true);status(tr("status_loading_history"));
  try{const before=Number(model.history.next_before);const result=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/history?limit=${HISTORY_PAGE_SIZE}&before=${encodeURIComponent(String(before))}`);model.history={...result,events:(model.history?.events||[]).concat(result.events||[]),returned:((model.history?.events||[]).length+(result.events||[]).length)};renderPlay();status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function toggleHistory(){
  if(!model.instanceId)return;
  if(model.historyExpanded){model.historyExpanded=false;renderPlay();return}
  if(model.history?.events?.length){model.historyExpanded=true;renderPlay();return}
  busy(true);status(tr("status_loading_history"));
  try{const result=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/history?limit=${HISTORY_PAGE_SIZE}`);model.history=result;model.historyExpanded=true;renderPlay();status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function replayAt(ticks){
  if(!model.instanceId)return;
  busy(true);status(tr("status_replaying"));
  try{const result=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/replay?at_ticks=${encodeURIComponent(String(ticks))}`);model.replay=result;model.historyExpanded=false;model.stageFocus=false;renderPlay();status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
function exitReplay(){if(!model.replay)return;model.replay=null;model.historyExpanded=Boolean(model.history?.events?.length);renderPlay()}
$("stage-replay-exit").addEventListener("click",exitReplay);
$("chronicle-expand").addEventListener("click",toggleHistory);$("chronicle-more").addEventListener("click",loadMoreHistory);
"""
