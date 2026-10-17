"""Worldline fork controls for the Player World Stage.

A fork creates a real Kernel child branch and a detached Player handle; the
script then leaves the current session and returns to the plaza so the new
worldline can be resumed from recent sessions.
"""

# ruff: noqa: E501

WORLDLINE_SCRIPT = r"""
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
"""
