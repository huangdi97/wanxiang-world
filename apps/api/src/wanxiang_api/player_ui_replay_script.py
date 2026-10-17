"""Historical replay controls for the Player World Stage.

Classic scripts share one global lexical environment, so this module can use the
helpers (`$`, `tr`, `api`, `busy`) and the `model` object declared by
``player_ui_script.SCRIPT`` as long as the document loads that script first.
"""

# ruff: noqa: E501

REPLAY_SCRIPT = r"""
async function replayAt(ticks){
  if(!model.instanceId)return;
  busy(true);status(tr("status_replaying"));
  try{const result=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/replay?at_ticks=${encodeURIComponent(String(ticks))}`);model.replay=result;model.stageFocus=false;renderPlay();status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
function exitReplay(){if(!model.replay)return;model.replay=null;renderPlay()}
$("stage-replay-exit").addEventListener("click",exitReplay);
"""
