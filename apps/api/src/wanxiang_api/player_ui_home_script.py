"""Home and plaza rendering for the Player Experience (classic shared script).

Classic scripts share one global lexical environment, so this module may use the
helpers (`$`, `tr`, `safe`, `shown`, `tags`, `characterLine`) declared by
``player_ui_script.SCRIPT``: the asset loads this script first and every function
here only runs after the whole document has loaded.
"""

# ruff: noqa: E501

HOME_SCRIPT = r"""
function renderContinue(){
  const item=model.plaza?.continue;const slot=$("continue-slot");const home=$("home-view");
  if(home)home.classList.toggle("has-continue",Boolean(item));
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
  const setting=item.setting||{},visual=item.visual||{},uri=visual.data_uri||"";
  const tier=visual.tier?String(visual.tier).toLowerCase():"";
  const chip=tier?`<small>${safe(tr("visual_tier_short_"+tier))}</small>`:"";
  const art=uri?`<span class="world-card-art"><img src="${safe(uri)}" alt="${safe(tr("world_card_visual_alt",{world:item.name}))}" loading="lazy">${chip}</span>`:`<span class="world-card-art is-empty"><span class="world-card-art-note">${safe(tr("world_card_no_visual"))}</span></span>`;
  const place=setting.location||setting.region||"";
  const ticks=setting.time&&typeof setting.time==="object"?(setting.time.ticks??null):(setting.time??null);
  const facts=[];
  if(place)facts.push(`<span>${safe(tr("world_card_place",{place}))}</span>`);
  if(ticks!==null&&ticks!==undefined&&ticks!=="")facts.push(`<span>${safe(tr("world_card_time",{time:ticks}))}</span>`);
  if(setting.happening)facts.push(`<span>${safe(tr("world_card_happening",{event:setting.happening}))}</span>`);
  const state=item.can_continue?tr("world_card_continue"):tr("world_card_enter");
  return `<button class="world-card" data-profile="${safe(item.profile_id)}">${art}<span class="world-card-body"><span class="world-card-top"><span>${safe(tr("scenario_label"))}</span><span class="${item.can_continue?"world-card-state is-continue":"world-card-state"}">${safe(state)}</span></span><h3>${safe(item.name)}</h3><p>${safe(item.description)}</p>${facts.length?`<span class="world-card-facts">${facts.join(safe(tr("meta_separator")))}</span>`:`<span class="world-card-facts is-empty">${safe(tr("world_card_no_facts"))}</span>`}<span class="tag-row">${tags(item.tags)}</span>${countParts.length?`<span class="world-card-meta">${countParts.join(safe(tr("meta_separator")))}</span>`:""}<span class="world-card-foot"><span>${safe(tr("enter_world"))}</span><span aria-hidden="true">↗</span></span></span></button>`;
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
  list.querySelectorAll("[data-profile]").forEach(node=>node.addEventListener("click",()=>openWorld(node.dataset.profile)));$("world-list-status").textContent=tr("world_count",{count:items.length});
}
function renderPlaza(){
  renderContinue();renderWorlds();renderHomeShelves();
  document.querySelectorAll(".filter-button").forEach(node=>{const selected=node.dataset.filter===model.filter;node.classList.toggle("is-active",selected);node.setAttribute("aria-pressed",String(selected))});
}
"""
