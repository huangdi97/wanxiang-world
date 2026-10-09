"""Browser behavior for the Player Experience; it only calls player routes."""

# ruff: noqa: E501

SCRIPT = r"""
const USER="studio";
const i18n=window.__PLAYER_I18N__||{locale:"zh-CN",strings:{}};
const LOCALE=i18n.locale||"zh-CN";
const tr=(key,values={})=>String(i18n.strings?.[key]??key).replace(/\{(\w+)\}/g,(_,name)=>String(values[name]??""));
const model={plaza:null,characters:[],world:null,view:null,instanceId:"",filter:"all",query:"",selectedCharacter:"",placeQuery:"",placeLimit:36};
const $=id=>document.getElementById(id);
const safe=value=>String(value??"").replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));
const shown=(value,emptyKey="not_recorded")=>value===null||value===undefined||value===""?tr(emptyKey):String(value);
const headers={"content-type":"application/json","x-wanxiang-user":USER,"x-wanxiang-locale":LOCALE};
const errorCopy={
  "embodiment_lease_conflict":"error_lease_conflict",
  "playable runtime is not configured":"error_runtime",
  "not found":"error_not_found",
  "embodiment requires a character":"error_need_character",
  "only an embodied actor may submit a world action":"error_need_embodiment",
  "no_allowed_affordance":"error_no_affordance",
  "unsafe_intent_text":"error_unsafe",
  "multiple_affordances":"error_multiple"
};
function humanError(payload){
  const code=typeof payload?.code==="string"?payload.code:"";
  if(errorCopy[code])return tr(errorCopy[code]);
  const raw=typeof payload?.detail==="string"?payload.detail:typeof payload?.message==="string"?payload.message:"";
  for(const key of Object.keys(errorCopy))if(raw.includes(key))return tr(errorCopy[key]);
  if(raw.includes("missing_fields"))return tr("error_missing");
  return tr("error_generic");
}
async function api(path,options={}){
  const response=await fetch(path,{...options,headers:{...headers,...(options.headers||{})}});
  const payload=await response.json().catch(()=>({}));
  if(!response.ok)throw new Error(humanError(payload));
  return payload;
}
function status(message,isError=false){
  const node=$("status");node.textContent=message||"";node.classList.toggle("is-error",isError);
}
function busy(value){document.body.setAttribute("aria-busy",value?"true":"false")}
function view(name){
  document.querySelectorAll(".view").forEach(node=>node.classList.toggle("is-active",node.id===name));
  if(name!=="home-view")document.querySelectorAll(".nav-button").forEach(node=>node.classList.remove("is-active"));
  window.scrollTo({top:0,behavior:"smooth"});
}
function tags(items){return (items||[]).map(item=>`<span class="tag">${safe(item)}</span>`).join("")}
function worldById(profileId){return (model.plaza?.worlds||[]).find(item=>item.profile_id===profileId)}
function renderContinue(){
  const item=model.plaza?.continue;const slot=$("continue-slot");
  if(!item){slot.hidden=true;slot.innerHTML="";return}
  slot.hidden=false;
  const line=tr("continue_line",{world:item.world_name,character:item.character_name,time:item.time?.ticks??0});
  const location=tr("continue_location",{location:shown(item.last_location)});
  const leave=item.leave_time?tr("continue_leave_time",{time:item.leave_time.ticks}):tr(item.status==="active"?"session_active":"continue_no_new_events");
  const events=item.events_since_leave||[];const since=events.length?tr("continue_since_leave",{count:events.length}):tr("continue_no_new_events");
  const change=item.last_change?.summary?tr("continue_last_change",{change:item.last_change.summary}):"";
  slot.innerHTML=`<div class="continue-strip"><div class="continue-copy"><strong>${safe(tr("continue_heading"))}</strong><p>${safe(line)}</p><div class="continue-meta"><span>${safe(location)}</span><span>${safe(leave)}</span><span>${safe(since)}</span>${change?`<span>${safe(change)}</span>`:""}</div></div><button class="secondary-button" data-continue="${safe(item.instance_id)}">${safe(tr("continue_button"))}</button></div>`;
  slot.querySelector("[data-continue]").addEventListener("click",()=>continueWorld(item.instance_id));
}
function card(item,shelf=false){
  const counts=item.counts||{};const countParts=[];
  if(counts.characters)countParts.push(`${safe(counts.characters)} ${safe(tr("count_characters"))}`);
  if(counts.events)countParts.push(`${safe(counts.events)} ${safe(tr("count_events"))}`);
  return `<button class="world-card" data-profile="${safe(item.profile_id)}"><span class="world-card-top"><span>${safe(tr("scenario_label"))}</span><span>${safe(item.status||tr("world_ready"))}</span></span><h3>${safe(item.name)}</h3><p>${safe(item.description)}</p><span class="tag-row">${tags(item.tags)}</span>${countParts.length?`<span class="world-card-meta">${countParts.join(safe(tr("meta_separator")))}</span>`:""}<span class="world-card-foot"><span>${safe(tr("enter_world"))}</span><span aria-hidden="true">↗</span></span></button>`;
}
function filteredWorlds(){
  const all=model.plaza?.worlds||[];
  const recentIds=new Set((model.plaza?.recent_sessions||[]).map(item=>item.profile_id));
  const source=model.filter==="mine"?model.plaza?.my_worlds||[]:model.filter==="public"?all.filter(item=>item.is_public):model.filter==="recent"?all.filter(item=>recentIds.has(item.profile_id)):all;
  const query=model.query.trim().toLowerCase();
  return source.filter(item=>!query||`${item.name} ${item.description} ${(item.tags||[]).join(" ")}`.toLowerCase().includes(query));
}
function renderRecent(){
  const list=$("recent-list"),items=model.plaza?.recent_sessions||[];
  if(!items.length){list.innerHTML=`<div class="empty-state"><strong>${safe(tr("no_recent_title"))}</strong><p>${safe(tr("no_recent_body"))}</p></div>`;return}
  list.innerHTML=items.map(item=>{
    const events=item.events_since_leave||[];const last=item.last_change?.summary||tr("not_recorded");
    return `<article class="session-card"><div class="session-card-head"><div><span class="eyebrow">${safe(tr(item.status==="active"?"session_active":"session_saved"))}</span><h4>${safe(item.world_name)}</h4><p>${safe(item.character_name)}</p></div><button class="secondary-button" data-continue="${safe(item.instance_id)}">${safe(tr("continue_button"))}</button></div><dl class="session-facts"><div><dt>${safe(tr("location_value_label"))}</dt><dd>${safe(shown(item.last_location))}</dd></div><div><dt>${safe(tr("current_world_time_label"))}</dt><dd>${safe(item.time?.ticks??0)}</dd></div><div><dt>${safe(tr("leave_time_label"))}</dt><dd>${safe(item.leave_time?.ticks??tr("not_recorded"))}</dd></div><div><dt>${safe(tr("events_since_leave_label"))}</dt><dd>${safe(events.length?tr("continue_since_leave",{count:events.length}):tr("continue_no_new_events"))}</dd></div></dl><p class="session-last-change"><span>${safe(tr("last_change_label"))}</span>${safe(last)}</p></article>`;
  }).join("");
  list.querySelectorAll("[data-continue]").forEach(node=>node.addEventListener("click",()=>continueWorld(node.dataset.continue)));
}
function renderHomeShelves(){
  const mine=model.plaza?.my_worlds||[];$("my-world-list").innerHTML=mine.length?mine.map(card).join(""):`<div class="empty-state"><strong>${safe(tr("no_my_worlds_title"))}</strong><p>${safe(tr("no_my_worlds_body"))}</p></div>`;
  $("home-character-list").innerHTML=model.characters.length?model.characters.slice(0,3).map(item=>characterLine(item)).join(""):`<div class="empty-state"><strong>${safe(tr("no_characters_title"))}</strong><p>${safe(tr("no_characters_body"))}</p></div>`;
  $("my-world-list").querySelectorAll("[data-profile]").forEach(node=>node.addEventListener("click",()=>openWorld(node.dataset.profile)));
  renderRecent();
}
function renderWorlds(){
  const list=$("world-list"),items=filteredWorlds();
  const titleKey=model.query?"empty_search_title":"empty_worlds_title";
  const bodyKey=model.query?"empty_search_body":"empty_worlds_body";
  list.innerHTML=items.length?items.map(card).join(""):`<div class="empty-state"><strong>${safe(tr(titleKey))}</strong><p>${safe(tr(bodyKey))}</p></div>`;
  list.querySelectorAll("[data-profile]").forEach(node=>node.addEventListener("click",()=>openWorld(node.dataset.profile)));
}
function renderPlaza(){
  renderContinue();renderWorlds();renderHomeShelves();
  document.querySelectorAll(".filter-button").forEach(node=>node.classList.toggle("is-active",node.dataset.filter===model.filter));
}
function characterLine(item,choice=false){
  const selected=model.selectedCharacter===item.character_id?" checked":"";
  const meta=[item.identity,item.stance,item.starting_location].filter(Boolean).join(tr("meta_separator"));
  const intro=item.intro||tr("no_intro");const boundary=item.knowledge_boundary||tr("not_recorded");
  if(choice)return `<label class="character-choice"><input type="radio" name="character" value="${safe(item.character_id)}"${selected}><span class="character-main"><strong>${safe(item.name)}</strong><span>${safe(meta||tr("character_profile"))}</span><span>${safe(intro)}</span><span class="character-knowledge"><b>${safe(tr("knowledge_boundary_label"))}：</b>${safe(boundary)}</span></span><span class="character-action">${safe(tr("enter_as_character"))}</span></label>`;
  return `<article class="form-panel character-card"><div class="character-card-head"><strong>${safe(item.name)}</strong><span class="tag">${safe(tr("become_character"))}</span></div><p class="muted">${safe(item.identity||tr("character_profile"))}</p><p class="muted">${safe(intro)}</p><p class="muted">${safe(item.stance||tr("stance_empty"))}${safe(tr("meta_separator"))}${safe(item.starting_location||tr("starting_location_empty"))}</p><p class="character-knowledge"><b>${safe(tr("knowledge_boundary_label"))}：</b>${safe(boundary)}</p></article>`;
}
function renderCharacterView(){
  const list=$("all-character-list");
  list.innerHTML=model.characters.length?model.characters.map(item=>characterLine(item)).join(""):`<div class="empty-state"><strong>${safe(tr("no_characters_title"))}</strong><p>${safe(tr("no_characters_body"))}</p></div>`;
}
function focusDetailVisual(item,galleryItems){
  if(!item)return;
  const image=$("detail-visual-image");
  const label=item.kind==="atlas"?tr("visual_atlas_label"):item.place_name||model.world?.world?.name||tr("world");
  image.hidden=false;image.src=item.data_uri;image.alt=label;image.dataset.selectedPlace=item.place_name||"";
  $("detail-visual-caption").textContent=item.kind==="atlas"?tr("visual_atlas_caption"):label;
  $("visual-gallery").querySelectorAll("[data-visual-index]").forEach(node=>node.setAttribute("aria-pressed",String(galleryItems[Number(node.dataset.visualIndex)]===item)));
  $("visual-places").querySelectorAll("[data-focus-place]").forEach(node=>node.setAttribute("aria-pressed",String(node.dataset.focusPlace===item.place_name)));
}
function renderVisualPlaceList(scenes,galleryItems,visual){
  const places=model.world?.world?.visual?.places||[],placeList=$("visual-places");
  const query=model.placeQuery.trim().toLocaleLowerCase();
  const matches=places.filter(item=>item.name.toLocaleLowerCase().includes(query));
  const visible=matches.slice(0,model.placeLimit);
  const selectedPlace=$("detail-visual-image").dataset.selectedPlace||"";
  placeList.innerHTML=visible.length?visible.map(item=>`<button class="visual-place" type="button" data-generated="${item.generated?"true":"false"}"${item.generated?` data-focus-place="${safe(item.name)}" aria-pressed="${selectedPlace===item.name?"true":"false"}"`:` data-generate-place="${safe(item.name)}"`}><span>${safe(item.name)}</span><span>${safe(tr(item.generated?"visual_place_ready":"visual_place_generate"))}</span></button>`).join(""):`<p class="muted">${safe(tr("visual_places_empty"))}</p>`;
  $("visual-place-count").textContent=tr("visual_place_count",{visible:visible.length,total:matches.length});
  $("visual-place-more").hidden=visible.length>=matches.length;
  placeList.querySelectorAll("[data-generate-place]").forEach(node=>node.addEventListener("click",()=>generateVisualPlace(node.dataset.generatePlace||"")));
  placeList.querySelectorAll("[data-focus-place]").forEach(node=>node.addEventListener("click",()=>{const item=scenes.find(scene=>scene.place_name===node.dataset.focusPlace);if(item)focusDetailVisual(item,galleryItems)}));
}
function renderDetail(preferredPlace=""){
  const world=model.world.world;
  const setting=world.setting||{};
  const scenes=world.visual?.scenes||[],topology=world.visual?.topology||[],atlas=world.visual?.atlas||null;const visual=(preferredPlace?scenes.find(item=>item.place_name===preferredPlace):null)||atlas||scenes[0]||null;const visualImg=$("detail-visual-image");visualImg.hidden=!visual;visualImg.dataset.selectedPlace=visual?.place_name||"";if(visual){visualImg.src=visual.data_uri;visualImg.alt=visual.kind==="atlas"?tr("visual_atlas_label"):visual.place_name||world.name;$("detail-visual-caption").textContent=visual.kind==="atlas"?tr("visual_atlas_caption"):visual.place_name||world.name}else{$("detail-visual-caption").textContent=tr("world_plate_copy")}
  const galleryItems=atlas?[atlas,...scenes]:scenes;const galleryWrap=$("visual-gallery-wrap"),gallery=$("visual-gallery");galleryWrap.hidden=!galleryItems.length;gallery.innerHTML=galleryItems.map((item,index)=>{const label=item.kind==="atlas"?tr("visual_atlas_label"):item.place_name||world.name;return `<button class="visual-thumb" type="button" data-visual-index="${index}" aria-pressed="${item===visual?"true":"false"}"><img alt="${safe(label)}" src="${safe(item.data_uri)}"><span>${safe(label)}</span></button>`}).join("");gallery.querySelectorAll("[data-visual-index]").forEach(node=>node.addEventListener("click",()=>{const item=galleryItems[Number(node.dataset.visualIndex)]||null;if(item)focusDetailVisual(item,galleryItems)}));const places=world.visual?.places||[],placesWrap=$("visual-places-wrap");placesWrap.hidden=!places.length;const placeSearch=$("visual-place-search");placeSearch.value=model.placeQuery;placeSearch.oninput=()=>{model.placeQuery=placeSearch.value;model.placeLimit=36;renderVisualPlaceList(scenes,galleryItems,visual)};$("visual-place-more").onclick=()=>{model.placeLimit+=36;renderVisualPlaceList(scenes,galleryItems,visual)};renderVisualPlaceList(scenes,galleryItems,visual);const relationsWrap=$("visual-relations-wrap"),relations=$("visual-relations");relationsWrap.hidden=!topology.length;relations.innerHTML=topology.map(item=>`<span class="visual-relation">${safe(item.from)} <b>→</b> ${safe(item.to)}</span>`).join("");$("detail-title").textContent=world.name;$("detail-plate-title").textContent=world.name;$("detail-description").textContent=world.description;$("detail-scenario").textContent=world.scenario.name;$("detail-opening").textContent=world.scenario.opening;$("detail-era").textContent=shown(setting.era);$("detail-location").textContent=shown(setting.location);$("detail-environment").textContent=shown(setting.environment);$("detail-time").textContent=shown(setting.time,"time_after_enter");$("detail-now").textContent=shown(setting.happening);$("detail-mode").textContent=world.mode||tr("mode_character");
  const list=$("character-list"),items=model.world.characters||[];
  list.innerHTML=items.length?items.map(item=>characterLine(item,true)).join(""):`<div class="empty-state"><strong>${safe(tr("no_compatible_title"))}</strong><p>${safe(tr("no_compatible_body"))}</p><button type="button" class="text-button" data-open-characters>${safe(tr("create_character_from_world"))}</button></div>`;
  if(items.length&&!items.some(item=>item.character_id===model.selectedCharacter)){model.selectedCharacter=items[0].character_id;const radio=list.querySelector("input");if(radio)radio.checked=true}
  list.querySelectorAll('input[name="character"]').forEach(node=>node.addEventListener("change",()=>{model.selectedCharacter=node.value}));
}
async function openWorld(profileId){
  busy(true);status(tr("status_open_world"));view("detail-view");
  try{model.world=await api(`/experience/player/worlds/${encodeURIComponent(profileId)}`);model.selectedCharacter="";model.placeQuery="";model.placeLimit=36;renderDetail();status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function generateVisualPlace(place){
  const profile=model.world?.world?.profile_id;if(!profile||!place)return;
  busy(true);status(tr("status_generating_scene",{place}));
  try{const result=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/visuals`,{method:"POST",body:JSON.stringify({place_name:place})});model.world.world=result.world;renderDetail(place);status(tr("status_scene_ready",{place}))}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function enterWorld(){
  const character=document.querySelector('input[name="character"]:checked')?.value;
  if(!character){status(tr("error_need_character"),true);return}
  const profile=model.world.world.profile_id;busy(true);status(tr("status_open_world"));
  try{const result=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/enter`,{method:"POST",body:JSON.stringify({mode:"embodiment",session_id:`m95_player_${Date.now()}`,character_id:character})});model.instanceId=result.instance_id;model.view=result.view;renderPlay();view("play-view");status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function enterObserver(){
  const profile=model.world.world.profile_id;busy(true);status(tr("status_open_world"));
  try{const result=await api(`/experience/player/worlds/${encodeURIComponent(profile)}/enter`,{method:"POST",body:JSON.stringify({mode:"observer",session_id:`observer_${Date.now()}`})});model.instanceId=result.instance_id;model.view=result.view;renderPlay();view("play-view");status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
function rowList(items,emptyKey,renderer){return items?.length?items.map(renderer).join(""):`<li class="muted">${safe(tr(emptyKey))}</li>`}
function relationLabel(value){const raw=String(value||"").toLowerCase();if(raw.includes("friend"))return tr("relation_friend");if(raw.includes("family"))return tr("relation_family");if(raw.includes("work"))return tr("relation_work");return tr("relation_default")}
function renderPlay(){
  const v=model.view||{},w=v.world||{};const visual=v.visual_scene||null;const stage=$("world-stage"),frame=$("scene-visual-frame"),visualImg=$("scene-visual-image");frame.hidden=!visual;stage?.classList.toggle("has-visual",Boolean(visual));if(visual){visualImg.src=visual.data_uri;visualImg.alt=visual.place_name||w.name||tr("world");const groundingKey=visual.grounding==="current_location"?"visual_current_scene":visual.grounding==="entry_location"?"visual_entry_scene":"visual_world_preview";$("scene-visual-caption").textContent=tr(groundingKey,{place:visual.place_name||shown(v.location)})}
  const clues=visual?.clues||[],clueWrap=$("scene-visual-clues-wrap"),clueNode=$("scene-visual-clues");clueWrap.hidden=!clues.length;clueNode.innerHTML=clues.map(item=>`<span class="scene-clue">${safe(item)}</span>`).join("");
  const observer=v.session?.entry_mode==="observer";$("play-mode").textContent=tr(observer?"observer_mode":"mode_character");$("play-mode-hint").textContent=observer?tr("observer_mode_hint"):"";$("action-input").disabled=observer;$("send-action").disabled=observer;document.querySelectorAll(".suggestion").forEach(node=>{node.disabled=observer});
  $("play-world-name").textContent=w.name||tr("world");$("play-world-description").textContent=w.description||"";$("play-region").textContent=shown(v.region);$("play-time").textContent=tr("world_time",{time:v.time?.ticks??0});$("play-location").textContent=shown(v.location);$("play-environment").textContent=shown(v.environment);$("play-weather").textContent=shown(v.weather);
  const event=v.current_event;$("current-event").innerHTML=event?`<strong>${safe(event.name)}</strong><span>${safe(event.description||tr("event_response_fallback"))}</span>`:`<span class="muted">${safe(tr("event_waiting"))}</span>`;
  $("narrative").textContent=v.narrative||tr("narrative_waiting");
  $("opportunity-list").innerHTML=rowList(v.opportunities,"opportunities_empty",item=>`<li><strong>${safe(item.name)}</strong><span class="muted">${safe(item.description||item.status||tr("event_response_fallback"))}</span></li>`);
  $("people-list").innerHTML=rowList(v.present_people,"people_empty",item=>`<li><strong>${safe(item.name)}</strong><span class="muted">${safe(item.role||item.status||tr("person_in_scene"))}</span></li>`);
  $("change-list").innerHTML=rowList(v.recent_changes,"changes_empty",item=>`<li><strong>${safe(item.summary)}</strong><span class="muted">${safe(item.category||tr("status_category"))}</span></li>`);
  $("chronicle-list").innerHTML=rowList(v.chronicle,"chronicle_empty",item=>`<li><strong>${safe(tr("moment",{time:item.time}))}</strong><span class="muted">${safe(item.summary)}</span></li>`);
  const p=v.player||{};$("player-name").textContent=observer?tr("observer_mode"):p.name||tr("your_character");$("player-status").textContent=shown(p.status);$("player-position").textContent=shown(p.location);$("player-items").innerHTML=rowList(p.items,"items_empty",item=>`<li>${safe(item)}</li>`);$("player-goals").innerHTML=rowList(p.goals,"goals_empty",item=>`<li>${safe(item)}</li>`);$("player-memory").textContent=p.memories?.length?tr("memory_count",{count:p.memories.length}):tr("memory_empty");$("memory-list").innerHTML=rowList(p.memories,"memory_empty",item=>`<li>${safe(item)}</li>`);
  $("relation-list").innerHTML=rowList(v.relations,"relations_empty",item=>`<li>${safe(item.from)} ${safe(tr("meta_separator"))}${safe(relationLabel(item.label))}${safe(tr("meta_separator"))}${safe(item.to)}</li>`);
}
async function continueWorld(instanceId){
  busy(true);status(tr("status_returning"));
  try{const result=await api(`/experience/player/instances/${encodeURIComponent(instanceId)}/continue`,{method:"POST"});model.instanceId=result.instance_id;model.view=result.view;renderPlay();view("play-view");status("")}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function sendAction(){
  const input=$("action-input"),text=input.value.trim();if(!text){status(tr("action_empty"),true);input.focus();return}
  busy(true);status(tr("status_world_response"));
  try{const result=await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/action`,{method:"POST",body:JSON.stringify({text})});model.view=result.view;renderPlay();input.value="";status(result.changed?tr("status_world_recorded"):tr("status_world_no_change"));input.focus()}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function leaveWorld(){
  busy(true);status(tr("status_saving_position"));
  try{await api(`/experience/player/instances/${encodeURIComponent(model.instanceId)}/leave`,{method:"POST"});model.instanceId="";model.view=null;view("home-view");await loadHome();status(tr("status_home_returned"))}
  catch(error){status(error.message,true)}finally{busy(false)}
}
async function loadHome(){
  busy(true);status(tr("status_loading_home"));
  try{const [plaza,characters]=await Promise.all([api("/experience/player/plaza"),api("/experience/player/characters")]);model.plaza=plaza;model.characters=characters.characters||[];renderPlaza();renderCharacterView();status("")}
  catch(error){$("world-list").innerHTML=`<div class="error-state"><strong>${safe(tr("plaza_unavailable_title"))}</strong><p>${safe(error.message)}</p><button class="secondary-button" id="retry-home">${safe(tr("retry"))}</button></div>`;$("retry-home").addEventListener("click",loadHome);status(error.message,true)}finally{busy(false)}
}
async function createCharacter(event){
  event.preventDefault();const form=event.currentTarget;const values=id=>$(id).value.trim();
  const body={display_name:values("character-name"),identity:values("character-identity"),intro:values("character-intro"),stance:values("character-stance"),starting_location:values("character-location"),knowledge_boundary:values("character-knowledge"),compatible_profile_ids:model.world?.world?.profile_id?[model.world.world.profile_id]:[]};
  if(!body.display_name){status(tr("character_name_required"),true);return}
  busy(true);status(tr("status_saving_character"));
  try{const result=await api("/experience/player/characters",{method:"POST",body:JSON.stringify(body)});model.characters.push(result.character);form.reset();renderCharacterView();if(model.world){const refreshed=await api(`/experience/player/worlds/${encodeURIComponent(model.world.world.profile_id)}`);model.world=refreshed;renderDetail()}status(tr("status_character_saved"))}
  catch(error){status(error.message,true)}finally{busy(false)}
}
document.querySelectorAll(".filter-button").forEach(node=>node.addEventListener("click",()=>{model.filter=node.dataset.filter;renderPlaza()}));
$("world-search").addEventListener("input",event=>{model.query=event.target.value;renderWorlds()});
$("enter-world").addEventListener("click",enterWorld);$("enter-observer").addEventListener("click",enterObserver);$("send-action").addEventListener("click",sendAction);$("leave-world").addEventListener("click",leaveWorld);$("character-form").addEventListener("submit",createCharacter);
$("create-character-inline").addEventListener("click",()=>{view("characters-view");document.querySelector('[data-nav="characters-view"]').classList.add("is-active");$("character-form-panel").open=true;$("character-name").focus()});
$("action-input").addEventListener("keydown",event=>{if(event.key==="Enter"&&!event.shiftKey){event.preventDefault();sendAction()}});
document.querySelectorAll(".suggestion").forEach(node=>node.addEventListener("click",()=>{$("action-input").value=node.dataset.action||"";$("action-input").focus()}));
document.querySelectorAll("[data-nav]").forEach(node=>node.addEventListener("click",()=>{view(node.dataset.nav);document.querySelectorAll(".nav-button").forEach(item=>item.classList.remove("is-active"));node.classList.add("is-active");if(node.dataset.mode==="mine"){model.filter="mine";renderPlaza()}if(node.dataset.nav==="home-view")window.setTimeout(()=>$('plaza-panel').scrollIntoView({behavior:"smooth"}),20)}));
document.addEventListener("click",event=>{const target=event.target.closest("[data-open-characters]");if(target){view("characters-view");document.querySelector('[data-nav="characters-view"]').classList.add("is-active");$("character-form-panel").open=true}});
$("back-to-plaza").addEventListener("click",()=>{view("home-view");document.querySelectorAll(".nav-button").forEach(item=>item.classList.remove("is-active"));document.querySelector('[data-mode="mine"]')?.classList.remove("is-active");document.querySelector('[data-nav="home-view"]')?.classList.add("is-active");window.setTimeout(()=>$('plaza-panel').scrollIntoView({behavior:"smooth"}),20)});
$("home-enter").addEventListener("click",()=>window.setTimeout(()=>$('plaza-panel').scrollIntoView({behavior:"smooth"}),20));
const worldStage=$("world-stage");
if(worldStage&&!window.matchMedia("(prefers-reduced-motion: reduce)").matches){
  worldStage.addEventListener("pointermove",event=>{const rect=worldStage.getBoundingClientRect();const x=((event.clientX-rect.left)/rect.width-.5)*-10;const y=((event.clientY-rect.top)/rect.height-.5)*-6;worldStage.style.setProperty("--stage-x",`${x.toFixed(2)}px`);worldStage.style.setProperty("--stage-y",`${y.toFixed(2)}px`)});
  worldStage.addEventListener("pointerleave",()=>{worldStage.style.setProperty("--stage-x","0px");worldStage.style.setProperty("--stage-y","0px")});
}
loadHome();
"""
