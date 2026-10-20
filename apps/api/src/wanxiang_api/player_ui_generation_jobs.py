"""Embedded Player generation-job functions injected into the main browser script.

Keeping this as a string fragment preserves one JavaScript lexical scope while
keeping the Python host module under the repository maintainability limit.
"""

# ruff: noqa: E501

GENERATION_JOB_FUNCTIONS = r"""
async function loadSpatialStatus(profile){try{const result=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/spatial`);if(Number(result.rehydrated_attachments||0)>0&&model.world?.world?.profile_id===profile)model.world=await api(`/experience/player/worlds/${encodeURIComponent(profile)}`);return result}catch{return null}}
function stopSpatialAutoPoll(resetDelay=true){if(model.spatialPollTimer){window.clearTimeout(model.spatialPollTimer);model.spatialPollTimer=0}if(resetDelay)model.spatialPollDelay=SPATIAL_POLL_MIN_MS}
function pendingSpatialJobs(){return (model.spatialStatus?.spatial_jobs||[]).some(item=>["submitted","queued","running","verified"].includes(item.state))}
function scheduleSpatialAutoPoll(){
  stopSpatialAutoPoll(false);
  if(!document.querySelector("#detail-view.is-active")||!pendingSpatialJobs()){model.spatialPollDelay=SPATIAL_POLL_MIN_MS;return}
  const delay=Math.max(SPATIAL_POLL_MIN_MS,Math.min(SPATIAL_POLL_MAX_MS,Number(model.spatialPollDelay)||SPATIAL_POLL_MIN_MS));
  model.spatialPollTimer=window.setTimeout(()=>{model.spatialPollTimer=0;void refreshSpatialJobs(true)},delay);
  model.spatialPollDelay=Math.min(SPATIAL_POLL_MAX_MS,Math.round(delay*1.6));
}
function spatialStateLabel(value){return tr(`spatial_upgrade_state_${value||"submitted"}`)}
function renderSpatialPanel(scene){
  const panel=$("spatial-upgrade-panel"),submit=$("spatial-submit"),refresh=$("spatial-refresh"),copy=$("spatial-upgrade-copy"),jobsNode=$("spatial-job-list"),spatial=model.spatialStatus;const place=scene?.place_name||"";panel.hidden=!place||!spatial;if(panel.hidden){jobsNode.innerHTML="";return}
  const jobs=(spatial.spatial_jobs||[]).filter(item=>item.place_name===place),job=jobs[jobs.length-1]||null,generation=spatial.generation||{},ready=Boolean(scene?.spatial?.ready)||job?.state==="attached",pending=Boolean(job&&["submitted","queued","running","verified"].includes(job.state)),ambiguous=job?.state==="submission_ambiguous",terminal=Boolean(job&&["failed","cancelled","expired"].includes(job.state));
  const reasonKey={provider_not_configured:"spatial_upgrade_unavailable_provider",network_not_allowed:"spatial_upgrade_unavailable_network",source_external_processing_not_allowed:"spatial_upgrade_unavailable_rights",private_source_provider_not_safe:"spatial_upgrade_unavailable_privacy",budget_insufficient:"spatial_upgrade_unavailable_budget"}[generation.reason]||"spatial_upgrade_unavailable_provider";
  copy.textContent=ready?tr("spatial_upgrade_ready",{place,count:scene?.spatial?.asset_count||job?.asset_count||0}):pending?tr("spatial_upgrade_pending",{place,state:spatialStateLabel(job.state)}):ambiguous?tr("spatial_upgrade_ambiguous",{place}):terminal?tr("spatial_upgrade_terminal",{place,state:spatialStateLabel(job.state)}):generation.available?tr("spatial_upgrade_available",{place,cost:generation.cost_units||0,remaining:generation.budget_remaining||0}):tr(reasonKey);
  jobsNode.innerHTML=jobs.map(item=>`<span class="spatial-job-chip">${safe(item.place_name)} · ${safe(spatialStateLabel(item.state))}</span>`).join("");submit.hidden=ready||Boolean(job)||!generation.available;submit.dataset.place=place;refresh.hidden=!pending;
}
async function submitPanoramaPlace(place){const profile=model.world?.world?.profile_id;if(!profile||!place)return;busy(true);try{const result=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/panoramas`,{method:"POST",body:JSON.stringify({place_name:place})});if(result.world)model.world.world=result.world;await window.__WANXIANG_PANORAMA_UPGRADE__?.load(profile,api);renderDetail(place);status(tr("status_panorama_generated",{place}))}catch(error){status(error.message,true)}finally{busy(false)}}
async function submitSpatialPlace(place){const profile=model.world?.world?.profile_id;if(!profile||!place)return;stopSpatialAutoPoll();busy(true);try{await api(`/experience/player/worlds/${encodeURIComponent(profile)}/spatial`,{method:"POST",body:JSON.stringify({place_name:place})});model.spatialStatus=await loadSpatialStatus(profile);renderDetail(place);status(tr("status_spatial_submitted",{place}));scheduleSpatialAutoPoll()}catch(error){status(error.message,true)}finally{busy(false)}}
async function refreshSpatialJobs(automatic=false){
  const profile=model.world?.world?.profile_id;if(!profile||model.spatialPollBusy)return;
  model.spatialPollBusy=true;if(!automatic)busy(true);
  try{const jobs=model.spatialStatus?.spatial_jobs||[];for(const job of jobs.filter(item=>["submitted","queued","running","verified"].includes(item.state))){const result=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/spatial/${encodeURIComponent(job.submission_id)}`);if(result.world)model.world.world=result.world}model.spatialStatus=await loadSpatialStatus(profile);const selected=$("detail-visual-image").dataset.selectedPlace||"";renderDetail(selected);if(!automatic)status(tr("status_spatial_refreshed"))}
  catch(error){if(!automatic)status(error.message,true)}
  finally{model.spatialPollBusy=false;if(!automatic)busy(false);scheduleSpatialAutoPoll()}
}
"""
