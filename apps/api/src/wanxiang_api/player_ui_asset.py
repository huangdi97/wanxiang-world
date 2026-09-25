"""Self-contained Player Experience document served by FastAPI."""

# pyright: reportPrivateUsage=false

# ruff: noqa: E501

from html import escape

import wanxiang_substrate.playable.player_i18n as _player_i18n

from wanxiang_api.player_ui_script import SCRIPT
from wanxiang_api.player_ui_style import STYLE


def player_html(locale: str | None = None) -> str:
    """Return the Player document with one immutable, selected copy catalog."""

    copy = _player_i18n._copy_for(locale)

    def text(key: str) -> str:
        return escape(copy.text(key), quote=True)

    return (
        "<!doctype html>\n"
        f'<html lang="{copy.locale}" data-locale="{copy.locale}"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="theme-color" content="#14263b">'
        f"<title>{text('document_title')}</title>"
        f"<style>{STYLE}</style></head>\n"
        '<body aria-busy="false"><!--\n'
        "THESIS: Make the first meaningful step feel like entering a living place, not operating software.\n"
        "OWN-WORLD: Living Cartography field folio — cool paper, ink-blue rails, jade field notes, and coral action marks.\n"
        "STORY: The player moves from a world plate to a chosen role, then watches a real committed change return to the field.\n"
        "FIRST VIEWPORT: Brand promise, a geometric world plate, two clear entrances, and the next world within one scan.\n"
        "FORM: Grounded direction candidate 7 from seed 19e29434; deliberate folio rails and field marks replace dashboard tiles.\n"
        "FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, and DESIGN.md\n"
        "-->\n"
        f'<a class="skip-link" href="#main-content">{text("skip_link")}</a>\n'
        '<div class="site-shell"><header class="topbar">'
        f'<a class="brand" href="/">{text("brand")}<small>{text("brand_subtitle")}</small></a>'
        f'<nav class="main-nav" aria-label="{text("nav_aria")}">'
        f'<button class="nav-button is-active" data-view="home-view" data-nav="home-view">{text("nav_worlds")}</button>'
        f'<button class="nav-button" data-view="home-view" data-nav="home-view" data-mode="mine">{text("nav_my_worlds")}</button>'
        f'<button class="nav-button" data-view="characters-view" data-nav="characters-view">{text("nav_characters")}</button>'
        f'</nav><a class="creator-link" href="/studio/ui">{text("studio_link")}</a></header>'
        '<p class="status-line" id="status" role="status" aria-live="polite"></p>'
        '<main id="main-content">'
        '<section class="view is-active" id="home-view" aria-labelledby="home-heading">'
        f'<div class="hero"><div><h1 id="home-heading">{text("hero_title")}</h1>'
        f"<p>{text('hero_body')}</p>"
        f'<div class="hero-actions"><button class="primary-button" id="home-enter">{text("enter_world")}</button>'
        f'<a class="secondary-button" id="create-world" href="/studio/ui">{text("create_world")}</a></div></div>'
        f'<div class="field-map" aria-label="{text("map_aria")}"><div class="map-surface"></div>'
        '<span class="map-route one"></span><span class="map-route two"></span><span class="map-route three"></span>'
        '<span class="map-mark a"></span><span class="map-mark b"></span><span class="map-mark c"></span>'
        f'<div class="map-label">{text("map_label")}<span>{text("map_caption")}</span></div></div></div>'
        '<div id="continue-slot" hidden></div>'
        f'<section id="plaza-panel" aria-labelledby="plaza-heading"><div class="section-head"><div><h2 id="plaza-heading">{text("plaza_heading")}</h2>'
        f'<p>{text("plaza_intro")}</p></div></div><div class="shelf-head"><h3>{text("recommended_heading")}</h3><p>{text("recommended_intro")}</p></div>'
        f'<div class="toolbar"><label class="sr-only" for="world-search">{text("search_worlds")}</label><input class="search" id="world-search" aria-label="{text("search_worlds_aria")}">'
        f'<button class="filter-button is-active" data-filter="all">{text("filter_all")}</button><button class="filter-button" data-filter="public">{text("filter_public")}</button><button class="filter-button" data-filter="recent">{text("filter_recent")}</button><button class="filter-button" data-filter="mine">{text("filter_mine")}</button></div>'
        f'<div class="world-list" id="world-list" aria-live="polite"><div class="empty-state">{text("loading_worlds")}</div></div></section>'
        f'<div class="home-shelves"><section class="home-shelf" aria-labelledby="my-worlds-heading"><div class="shelf-head"><div><h3 id="my-worlds-heading">{text("my_worlds_heading")}</h3><p>{text("my_worlds_intro")}</p></div></div><div class="world-list compact-list" id="my-world-list"></div></section>'
        f'<section class="home-shelf" aria-labelledby="recent-heading"><div class="shelf-head"><div><h3 id="recent-heading">{text("recent_heading")}</h3><p>{text("recent_intro")}</p></div></div><div class="recent-list" id="recent-list"></div></section>'
        f'<section class="home-shelf" aria-labelledby="home-characters-heading"><div class="shelf-head"><div><h3 id="home-characters-heading">{text("home_characters_heading")}</h3><p>{text("home_characters_intro")}</p></div><button class="text-button" type="button" data-nav="characters-view">{text("view_all_characters")}</button></div><div class="character-list compact-list" id="home-character-list"></div></section></div></section>'
        f'<section class="view" id="detail-view" aria-labelledby="detail-title"><div class="section-head"><button class="text-button" id="back-to-plaza">{text("back_plaza")}</button></div>'
        f'<div class="detail-layout"><div class="detail-plate"><h2 id="detail-plate-title">{text("world")}</h2><p>{text("world_plate_copy")}</p></div>'
        f'<div class="detail-copy"><h2 id="detail-title">{text("world")}</h2><p id="detail-description"></p><dl class="detail-grid">'
        f'<div class="detail-cell"><dt>{text("scenario_label")}</dt><dd id="detail-scenario">{text("not_recorded")}</dd></div><div class="detail-cell"><dt>{text("era_label")}</dt><dd id="detail-era">{text("not_recorded")}</dd></div><div class="detail-cell"><dt>{text("location_label")}</dt><dd id="detail-location">{text("not_recorded")}</dd></div><div class="detail-cell"><dt>{text("environment_label")}</dt><dd id="detail-environment">{text("not_recorded")}</dd></div><div class="detail-cell"><dt>{text("time_label")}</dt><dd id="detail-time">{text("time_after_enter")}</dd></div><div class="detail-cell"><dt>{text("now_label")}</dt><dd id="detail-now">{text("not_recorded")}</dd></div></dl>'
        f'<div class="detail-mode"><span>{text("mode_label")}</span><strong id="detail-mode">{text("mode_character")}</strong></div>'
        f'<div class="form-panel"><strong>{text("recommended_opening")}</strong><p class="muted" id="detail-opening"></p></div></div></div>'
        f'<div class="selection"><div class="selection-head"><h3>{text("choose_character")}</h3><button class="text-button" id="create-character-inline" type="button">{text("create_character_inline")}</button></div><div class="character-list" id="character-list"></div>'
        f'<button class="primary-button" id="enter-world" type="button">{text("enter_as_character")}</button></div></section>'
        f'<section class="view" id="characters-view" aria-labelledby="characters-heading"><div class="section-head"><div><h2 id="characters-heading">{text("characters_heading")}</h2>'
        f'<p>{text("characters_intro")}</p></div></div><div class="character-list" id="all-character-list"></div>'
        f'<details class="form-panel" id="character-form-panel"><summary>{text("create_character_summary")}</summary><form id="character-form"><div class="form-grid">'
        f'<div class="field"><label for="character-name">{text("name_label")}</label><input id="character-name" required aria-label="{text("name_aria")}"></div>'
        f'<div class="field"><label for="character-identity">{text("identity_label")}</label><input id="character-identity" aria-label="{text("identity_aria")}"></div>'
        f'<div class="field form-wide"><label for="character-intro">{text("intro_label")}</label><textarea id="character-intro" aria-label="{text("intro_aria")}"></textarea></div>'
        f'<div class="field"><label for="character-stance">{text("stance_label")}</label><input id="character-stance" aria-label="{text("stance_aria")}"></div>'
        f'<div class="field"><label for="character-location">{text("starting_location_label")}</label><input id="character-location" aria-label="{text("starting_location_aria")}"></div>'
        f'<div class="field form-wide"><label for="character-knowledge">{text("knowledge_label")}</label><textarea id="character-knowledge" aria-label="{text("knowledge_aria")}"></textarea></div></div>'
        f'<button class="primary-button" type="submit">{text("save_character")}</button></form></details></section>'
        f'<section class="view" id="play-view" aria-labelledby="play-world-name"><div class="play-top"><div><h2 id="play-world-name">{text("world")}</h2><p id="play-world-description"></p></div>'
        f'<button class="secondary-button" id="leave-world" type="button">{text("leave_world")}</button></div><div class="play-grid">'
        f'<section class="play-panel scene-panel" aria-labelledby="scene-heading"><h3 id="scene-heading">{text("scene_heading")}</h3><div class="scene-status">'
        f'<div><span>{text("world")}</span><strong id="play-region">{text("not_recorded")}</strong></div><div><span>{text("time_label")}</span><strong id="play-time">{text("not_recorded")}</strong></div><div><span>{text("location_label")}</span><strong id="play-location">{text("not_recorded")}</strong></div>'
        f'<div><span>{text("environment_label")}</span><strong id="play-environment">{text("not_recorded")}</strong></div><div><span>{text("weather_label")}</span><strong id="play-weather">{text("not_recorded")}</strong></div></div>'
        f'<div class="narrative" id="narrative" aria-live="polite">{text("narrative_waiting")}</div><h3>{text("happening_heading")}</h3><div id="current-event" class="plain-list"></div><h3>{text("opportunities_heading")}</h3><ul class="plain-list" id="opportunity-list"></ul><h3>{text("people_heading")}</h3><ul class="plain-list" id="people-list"></ul></section>'
        f'<section class="play-panel" aria-labelledby="changes-heading"><h3 id="changes-heading">{text("changes_heading")}</h3><ul class="plain-list change-list" id="change-list"></ul><h3>{text("chronicle_heading")}</h3><ul class="plain-list" id="chronicle-list"></ul></section>'
        f'<aside class="play-panel player-panel" aria-labelledby="player-heading"><h3 id="player-heading">{text("your_character")}</h3><div class="player-stat"><span>{text("name_label")}</span><strong id="player-name">{text("your_character")}</strong></div><div class="player-stat"><span>{text("status_label")}</span><strong id="player-status">{text("not_recorded")}</strong></div><div class="player-stat"><span>{text("position_label")}</span><strong id="player-position">{text("not_recorded")}</strong></div><div class="player-stat"><span>{text("items_heading")}</span><ul class="plain-list" id="player-items"></ul></div><div class="player-stat"><span>{text("goals_heading")}</span><ul class="plain-list" id="player-goals"></ul></div><div class="player-stat"><span>{text("recent_memories_heading")}</span><strong id="player-memory">{text("memory_empty")}</strong><ul class="plain-list" id="memory-list"></ul></div><h3>{text("relations_heading")}</h3><ul class="plain-list" id="relation-list"></ul></aside></div>'
        f'<div class="action-bar"><label for="action-input">{text("action_label")}</label><input class="action-input" id="action-input" aria-label="{text("action_aria")}" autocomplete="off"><button class="primary-button" id="send-action" type="button">{text("action_send")}</button></div>'
        f'<div class="suggestions" aria-label="{text("suggestions_aria")}"><button class="suggestion" data-action="{text("action_awake_value")}">{text("suggestion_awake")}</button><button class="suggestion" data-action="{text("action_alert_value")}">{text("suggestion_alert")}</button><button class="suggestion" data-action="{text("action_rest_value")}">{text("suggestion_rest")}</button></div></section>'
        "</main></div>"
        f"<script>window.__PLAYER_I18N__={_player_i18n._serialize_copy(copy)};</script>"
        f"<script>{SCRIPT}</script></body></html>"
    )
