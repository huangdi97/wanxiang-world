"""Embedded Player generation-job functions injected into the main browser script.

Keeping this as a string fragment preserves one JavaScript lexical scope while
keeping the Python host module under the repository maintainability limit.
"""

# ruff: noqa: E501

GENERATION_JOB_FUNCTIONS = r"""
function currentSpatialProfile(){return model.view?.world?.profile_id||model.world?.world?.profile_id||""}
function syncLiveSpatialProjection(world){if(!world||model.view?.world?.profile_id!==world.profile_id)return;model.view.world=world;const live=model.view.visual_scene;if(!live?.place_name)return;const refreshed=(world.visual?.scenes||[]).find(item=>item.place_name===live.place_name);if(refreshed)model.view.visual_scene={...live,spatial:refreshed.spatial||null}}
function applySpatialWorldProjection(world){if(!world)return;if(model.world?.world?.profile_id===world.profile_id)model.world.world=world;syncLiveSpatialProjection(world)}
function rememberSpatialTicket(ticket){if(!ticket)return;const current=model.spatialStatus||{spatial_jobs:[]},jobs=(current.spatial_jobs||[]).filter(item=>item.submission_id!==ticket.submission_id);model.spatialStatus={...current,spatial_jobs:[...jobs,ticket]}}
async function loadSpatialStatus(profile){try{const result=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/spatial`);if(Number(result.rehydrated_attachments||0)>0){const refreshed=await api(`/experience/player/worlds/${encodeURIComponent(profile)}`);if(currentSpatialProfile()===profile&&refreshed?.world){model.world=refreshed;syncLiveSpatialProjection(refreshed.world)}}return result}catch{return null}}
function stopSpatialAutoPoll(resetDelay=true){if(model.spatialPollTimer){window.clearTimeout(model.spatialPollTimer);model.spatialPollTimer=0}if(resetDelay)model.spatialPollDelay=SPATIAL_POLL_MIN_MS}
function pendingSpatialJobs(){return (model.spatialStatus?.spatial_jobs||[]).some(item=>["submitted","queued","running","verified"].includes(item.state))}
function scheduleSpatialAutoPoll(){
  stopSpatialAutoPoll(false);
  if(!document.querySelector("#detail-view.is-active,#play-view.is-active")||!pendingSpatialJobs()){model.spatialPollDelay=SPATIAL_POLL_MIN_MS;return}
  const delay=Math.max(SPATIAL_POLL_MIN_MS,Math.min(SPATIAL_POLL_MAX_MS,Number(model.spatialPollDelay)||SPATIAL_POLL_MIN_MS));
  model.spatialPollTimer=window.setTimeout(()=>{model.spatialPollTimer=0;void refreshSpatialJobs(true)},delay);
  model.spatialPollDelay=Math.min(SPATIAL_POLL_MAX_MS,Math.round(delay*1.6));
}
function spatialStateLabel(value){return tr(`spatial_upgrade_state_${value||"submitted"}`)}
function spatialJobMeta(item){
  const parts=[tr("spatial_job_attempt",{attempt:Number(item.attempt||0)+1}),tr("spatial_job_reserved",{units:item.reserved_cost_units||0})];
  if(item.provider_usage_units!==null&&item.provider_usage_units!==undefined)parts.push(tr("spatial_job_usage",{units:item.provider_usage_units}));
  return parts.map(value=>`<span>${safe(value)}</span>`).join("");
}
function renderSpatialPanel(scene){
  const panel=$("spatial-upgrade-panel"),submit=$("spatial-submit"),refresh=$("spatial-refresh"),copy=$("spatial-upgrade-copy"),jobsNode=$("spatial-job-list"),spatial=model.spatialStatus;const place=scene?.place_name||"";panel.hidden=!place||!spatial;if(panel.hidden){jobsNode.innerHTML="";return}
  const jobs=(spatial.spatial_jobs||[]).filter(item=>item.place_name===place),job=jobs[jobs.length-1]||null,generation=spatial.generation||{},ready=Boolean(scene?.spatial?.ready)||job?.state==="attached",renderable=!ready||Boolean(window.__WANXIANG_SPATIAL_STAGE__?.supportsScene?.(scene)),pending=Boolean(job&&["submitted","queued","running","verified"].includes(job.state)),ambiguous=job?.state==="submission_ambiguous",terminal=Boolean(job&&["failed","cancelled","expired"].includes(job.state)),cancelPending=Boolean(job?.cancellation_requested);
  const reasonKey={provider_not_configured:"spatial_upgrade_unavailable_provider",network_not_allowed:"spatial_upgrade_unavailable_network",source_external_processing_not_allowed:"spatial_upgrade_unavailable_rights",private_source_provider_not_safe:"spatial_upgrade_unavailable_privacy",budget_insufficient:"spatial_upgrade_unavailable_budget"}[generation.reason]||"spatial_upgrade_unavailable_provider";
  copy.textContent=ready&&!renderable?tr("spatial_upgrade_ready_unrenderable",{place}):ready?tr("spatial_upgrade_ready",{place,count:scene?.spatial?.asset_count||job?.asset_count||0}):cancelPending?tr("spatial_upgrade_cancel_requested",{place}):pending?tr("spatial_upgrade_pending",{place,state:spatialStateLabel(job.state)}):ambiguous?tr("spatial_upgrade_ambiguous",{place}):terminal?tr("spatial_upgrade_terminal",{place,state:spatialStateLabel(job.state)}):generation.available?tr("spatial_upgrade_available",{place,cost:generation.cost_units||0,remaining:generation.budget_remaining||0}):tr(reasonKey);
  const budget=`<div class="spatial-budget-strip">${safe(tr("spatial_budget_summary",{reserved:generation.budget_reserved||0,total:generation.budget_total||0,remaining:generation.budget_remaining||0}))}</div>`;
  jobsNode.innerHTML=budget+jobs.map((item,index)=>{const active=["submitted","queued","running"].includes(item.state),canCancel=Boolean(spatial.cancellation_supported&&active&&!item.cancellation_requested);const cancel=canCancel?`<button class="text-button" type="button" data-spatial-cancel="${safe(item.submission_id)}">${safe(tr("spatial_upgrade_cancel"))}</button>`:"";return `<article class="spatial-job-card${index===jobs.length-1?" is-latest":""}"><div class="spatial-job-card-head"><strong>${safe(item.place_name)}</strong><span>${safe(spatialStateLabel(item.state))}</span></div><div class="spatial-job-meta">${spatialJobMeta(item)}</div><small>${safe(item.provider?.id||"")} · ${safe(item.provider?.version||"")}</small>${cancel}</article>`}).join("");
  jobsNode.querySelectorAll("[data-spatial-cancel]").forEach(node=>node.addEventListener("click",()=>cancelSpatialJob(node.dataset.spatialCancel||"")));
  submit.hidden=ready||ambiguous||pending||(!terminal&&Boolean(job))||!generation.available;submit.dataset.place=place;submit.dataset.retry=terminal?"true":"false";submit.textContent=tr(terminal?"spatial_upgrade_retry":"spatial_upgrade_submit");refresh.hidden=!pending;
}
async function submitPanoramaPlace(place){const profile=model.world?.world?.profile_id;if(!profile||!place)return;busy(true);try{const result=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/panoramas`,{method:"POST",body:JSON.stringify({place_name:place})});if(result.world)model.world.world=result.world;await window.__WANXIANG_PANORAMA_UPGRADE__?.load(profile,api);renderDetail(place);status(tr("status_panorama_generated",{place}))}catch(error){status(error.message,true)}finally{busy(false)}}
async function submitSpatialPlace(place,retryTerminal=false){const profile=model.world?.world?.profile_id;if(!profile||!place)return;stopSpatialAutoPoll();busy(true);try{const submitted=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/spatial`,{method:"POST",body:JSON.stringify({place_name:place,retry_terminal:Boolean(retryTerminal)})});rememberSpatialTicket(submitted.spatial);const refreshed=await loadSpatialStatus(profile);if(refreshed)model.spatialStatus=refreshed;renderDetail(place);status(tr("status_spatial_submitted",{place}));scheduleSpatialAutoPoll()}catch(error){status(error.message,true)}finally{busy(false)}}
async function cancelSpatialJob(submissionId){const profile=model.world?.world?.profile_id;if(!profile||!submissionId)return;stopSpatialAutoPoll();busy(true);try{const cancelled=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/spatial/${encodeURIComponent(submissionId)}/cancel`,{method:"POST"});rememberSpatialTicket(cancelled.spatial);const refreshed=await loadSpatialStatus(profile);if(refreshed)model.spatialStatus=refreshed;const selected=$("detail-visual-image").dataset.selectedPlace||"";renderDetail(selected);status(tr("status_spatial_cancel_requested"));scheduleSpatialAutoPoll()}catch(error){status(error.message,true)}finally{busy(false)}}
async function refreshSpatialJobs(automatic=false){
  const profile=currentSpatialProfile();if(!profile||model.spatialPollBusy)return;
  model.spatialPollBusy=true;if(!automatic)busy(true);
  try{const jobs=model.spatialStatus?.spatial_jobs||[];for(const job of jobs.filter(item=>["submitted","queued","running","verified"].includes(item.state))){const result=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/spatial/${encodeURIComponent(job.submission_id)}`);if(result.spatial)rememberSpatialTicket(result.spatial);if(result.world)applySpatialWorldProjection(result.world)}const refreshed=await loadSpatialStatus(profile);if(refreshed)model.spatialStatus=refreshed;if(document.querySelector("#detail-view.is-active")){const selected=$("detail-visual-image").dataset.selectedPlace||"";renderDetail(selected)}else if(document.querySelector("#play-view.is-active"))renderPlay();if(!automatic)status(tr("status_spatial_refreshed"))}
  catch(error){if(!automatic)status(error.message,true)}
  finally{model.spatialPollBusy=false;if(!automatic)busy(false);scheduleSpatialAutoPoll()}
}
"""
