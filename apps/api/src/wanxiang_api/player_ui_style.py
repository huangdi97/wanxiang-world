"""Styles for the isolated Chinese Player Experience surface."""

# ruff: noqa: E501

STYLE = r"""
:root{--ink:#14263b;--ink-soft:#496071;--paper:#f4f6f1;--paper-deep:#e6ece7;--line:#b8c8c3;--cobalt:#2d6f8f;--jade:#7aa99a;--coral:#e36b55;--ochre:#d39b47;--white:#fffef9;--shadow:0 18px 48px rgba(20,38,59,.12);--radius:14px;color-scheme:light}
*{box-sizing:border-box}
html{background:var(--paper);scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Sans SC","Source Han Sans SC","Microsoft YaHei",ui-sans-serif,sans-serif;line-height:1.55;letter-spacing:-.01em}
body:has(#play-view.is-active){background:#dfe9e5}
::selection{background:var(--coral);color:var(--white)}
::-webkit-scrollbar{width:11px;height:11px}
::-webkit-scrollbar-track{background:var(--paper-deep)}
::-webkit-scrollbar-thumb{background:#78928f;border:3px solid var(--paper-deep);border-radius:10px}
a{color:inherit;text-underline-offset:4px}
button,input,textarea{font:inherit}
button{cursor:pointer}
button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid var(--coral);outline-offset:3px}
.skip-link{position:absolute;left:1rem;top:-5rem;background:var(--ink);color:var(--white);padding:.65rem 1rem;z-index:10;border-radius:8px}
.skip-link:focus{top:1rem}
.site-shell{max-width:1440px;margin:auto;padding:0 3.5vw 5rem}
.topbar{min-height:76px;display:flex;align-items:center;gap:2rem;border-bottom:1px solid var(--line)}
.brand{display:inline-flex;align-items:baseline;gap:.55rem;text-decoration:none;font-weight:900;font-size:1.35rem;letter-spacing:-.04em;white-space:nowrap}
.brand small{font-size:.72rem;letter-spacing:.04em;color:var(--ink-soft);font-weight:700}
.main-nav{display:flex;gap:.25rem;align-items:center;flex-wrap:wrap}
.nav-button,.text-button{border:0;background:transparent;color:var(--ink-soft);padding:.55rem .75rem;border-radius:7px;font-weight:700}
.nav-button:hover,.nav-button.is-active,.text-button:hover{background:var(--ink);color:var(--white)}
.creator-link{margin-left:auto;color:var(--ink-soft);font-size:.9rem;font-weight:700;text-underline-offset:5px}
.hero{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(300px,.92fr);gap:clamp(2rem,7vw,8rem);align-items:center;padding:clamp(4rem,10vw,8rem) 0 4rem}
.hero h1{max-width:10ch;margin:0;font-size:clamp(2.5rem,6vw,5.4rem);line-height:1.03;letter-spacing:-.045em;font-weight:950}
.hero p{max-width:58ch;color:var(--ink-soft);font-size:1.1rem;margin:1.5rem 0 0}
.hero-actions{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:2rem}
.primary-button,.secondary-button{border:1px solid var(--ink);min-height:46px;padding:.7rem 1.1rem;border-radius:8px;font-weight:850;transition:transform .18s ease,box-shadow .18s ease,background .18s ease}
.primary-button{background:var(--ink);color:var(--white);box-shadow:0 8px 18px rgba(20,38,59,.16)}
.secondary-button{background:transparent;color:var(--ink)}
.primary-button:hover,.secondary-button:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(20,38,59,.14)}
.secondary-button:hover{background:var(--white)}
.field-map{min-height:350px;position:relative;overflow:hidden;background:#d4e1dc;border:1px solid #9db7b0;border-radius:var(--radius);box-shadow:var(--shadow);isolation:isolate}
.field-map:before,.field-map:after{content:"";position:absolute;z-index:-1;border:1px solid rgba(45,111,143,.47);border-radius:45% 55% 48% 52%;transform:rotate(-13deg)}
.field-map:before{inset:10% 12% 24% 5%;border-color:rgba(20,38,59,.32)}
.field-map:after{inset:35% -8% 3% 35%;transform:rotate(29deg);border-color:rgba(227,107,85,.52)}
.map-surface{position:absolute;inset:0;background:linear-gradient(135deg,transparent 49%,rgba(255,254,249,.35) 50%,transparent 51%),linear-gradient(38deg,transparent 47%,rgba(45,111,143,.18) 48%,transparent 49%)}
.map-route{position:absolute;height:1px;background:var(--cobalt);transform-origin:left center;opacity:.85}
.map-route.one{width:74%;left:9%;top:31%;transform:rotate(18deg)}
.map-route.two{width:62%;left:27%;top:69%;transform:rotate(-38deg);background:var(--coral)}
.map-route.three{width:45%;left:39%;top:24%;transform:rotate(76deg);background:var(--ochre)}
.map-mark{position:absolute;width:13px;height:13px;border:3px solid var(--white);background:var(--coral);border-radius:50%;box-shadow:0 0 0 1px var(--coral)}
.map-mark.a{left:21%;top:26%}.map-mark.b{left:66%;top:54%;background:var(--cobalt);box-shadow:0 0 0 1px var(--cobalt)}.map-mark.c{left:42%;top:77%;background:var(--ochre);box-shadow:0 0 0 1px var(--ochre)}
.map-label{position:absolute;left:1.4rem;bottom:1.25rem;font-weight:900;color:var(--ink);letter-spacing:.04em}
.map-label span{display:block;margin-top:.25rem;font-size:.75rem;font-weight:700;color:var(--ink-soft);letter-spacing:.01em}
.section-head{display:flex;justify-content:space-between;align-items:end;gap:1.5rem;margin:2.2rem 0 1rem}
.section-head h2{margin:0;font-size:clamp(1.65rem,3vw,2.6rem);line-height:1.1;letter-spacing:-.035em}
.section-head p{margin:0;color:var(--ink-soft);max-width:55ch}
.shelf-head{display:flex;justify-content:space-between;align-items:end;gap:1rem;margin:2rem 0 1rem}.shelf-head h3{margin:0;font-size:1.35rem;letter-spacing:-.025em}.shelf-head p{margin:.25rem 0 0;color:var(--ink-soft);max-width:58ch}
.view{display:none}.view.is-active{display:block}
.toolbar{display:flex;gap:.65rem;align-items:center;flex-wrap:wrap;margin:1rem 0 1.4rem}
.search{min-width:min(100%,330px);flex:1;padding:.75rem 1rem;border:1px solid var(--line);border-radius:8px;background:var(--white);color:var(--ink);caret-color:var(--coral)}
.filter-button{border:1px solid var(--line);background:transparent;color:var(--ink-soft);padding:.55rem .8rem;border-radius:999px;font-weight:750}
.filter-button:hover,.filter-button.is-active{background:var(--cobalt);border-color:var(--cobalt);color:var(--white)}
.world-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:1rem}
.world-card{display:flex;flex-direction:column;align-items:stretch;text-align:left;min-height:245px;padding:1.2rem;background:var(--white);border:1px solid var(--line);border-radius:var(--radius);color:var(--ink);box-shadow:0 7px 20px rgba(20,38,59,.06);transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
.world-card:hover{transform:translateY(-4px);border-color:var(--cobalt);box-shadow:var(--shadow)}
.world-card-top{display:flex;justify-content:space-between;gap:1rem;color:var(--ink-soft);font-size:.74rem;font-weight:850;letter-spacing:.08em;text-transform:uppercase}
.world-card h3{margin:1.5rem 0 .4rem;font-size:1.55rem;line-height:1.15;letter-spacing:-.03em}
.world-card p{margin:0;color:var(--ink-soft);max-width:42ch}
.tag-row{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:1.15rem}
.tag{padding:.26rem .5rem;border-radius:999px;background:#e5eee9;color:#315a5c;font-size:.75rem;font-weight:800}
.world-card-meta{display:block;margin-top:1rem;color:var(--ink-soft);font-size:.8rem;font-weight:750}
.world-card-foot{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:1.4rem;color:var(--cobalt);font-weight:900}
.home-shelves{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2.5rem 1.25rem;margin-top:3.25rem}.home-shelf{min-width:0}.compact-list{grid-template-columns:1fr}.compact-list .world-card{min-height:210px}.recent-list{display:grid;gap:.8rem}
.empty-state,.error-state{padding:2.2rem;background:var(--white);border:1px dashed var(--line);border-radius:var(--radius);color:var(--ink-soft)}
.error-state{border-color:#d99b91;color:#8b3f35;background:#fff8f5}
.continue-strip{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin:0 0 3rem;padding:1.2rem 1.35rem;background:var(--ink);color:var(--white);border-radius:var(--radius);box-shadow:var(--shadow)}
.continue-strip p{margin:.2rem 0 0;color:#c8d6d7}.continue-strip strong{font-size:1.1rem}
.continue-copy{min-width:0}.continue-meta{display:flex;gap:.45rem .9rem;flex-wrap:wrap;margin-top:.65rem;color:#c8d6d7;font-size:.8rem}.continue-meta span{max-width:34ch}
.session-card{padding:1rem 1.1rem;background:var(--white);border:1px solid var(--line);border-radius:12px;box-shadow:0 7px 20px rgba(20,38,59,.05)}.session-card-head{display:flex;justify-content:space-between;align-items:start;gap:1rem}.session-card h4{margin:.2rem 0 0;font-size:1.2rem}.session-card-head p{margin:.1rem 0 0;color:var(--ink-soft)}.eyebrow{color:var(--coral);font-size:.72rem;font-weight:900;letter-spacing:.08em}.session-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.65rem;margin:1rem 0 0}.session-facts div{padding:.65rem .75rem;background:var(--paper-deep);border-radius:9px}.session-facts dt{color:var(--ink-soft);font-size:.73rem;font-weight:800}.session-facts dd{margin:.2rem 0 0;font-weight:800}.session-last-change{margin:.9rem 0 0;color:var(--ink-soft);font-size:.86rem}.session-last-change span{display:block;color:var(--ink);font-size:.73rem;font-weight:850;margin-bottom:.15rem}
.detail-layout{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:2rem;align-items:start}
.detail-plate{min-height:310px;position:relative;background:var(--cobalt);color:var(--white);border-radius:var(--radius);padding:1.5rem;overflow:hidden;box-shadow:var(--shadow)}
.detail-plate:after{content:"";position:absolute;width:220px;height:220px;right:-45px;bottom:-90px;border:1px solid rgba(255,254,249,.42);border-radius:50%;box-shadow:0 0 0 24px rgba(255,254,249,.07),0 0 0 48px rgba(255,254,249,.05)}
.detail-plate h2{position:relative;z-index:1;margin:5rem 0 0;font-size:clamp(2rem,4vw,3.8rem);letter-spacing:-.05em;line-height:1.05}
.detail-plate p{position:relative;z-index:1;color:#d6e6e3;max-width:42ch}
.detail-copy h2{margin:0;font-size:2rem;letter-spacing:-.035em}.detail-copy>p{color:var(--ink-soft);font-size:1.05rem}.detail-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin:1.5rem 0}.detail-cell{padding:1rem;background:var(--paper-deep);border-radius:10px}.detail-cell dt{color:var(--ink-soft);font-size:.8rem;font-weight:800}.detail-cell dd{margin:.45rem 0 0;font-weight:850}
.detail-mode{display:flex;justify-content:space-between;gap:1rem;padding:.8rem 1rem;background:#e3eee9;border-radius:10px}.detail-mode span{color:var(--ink-soft);font-size:.8rem;font-weight:800}.detail-mode strong{font-size:.9rem}
.selection{margin-top:2.5rem}.selection h3{font-size:1.25rem;margin:0 0 1rem}.character-list{display:grid;gap:.75rem}.character-choice{display:flex;align-items:center;gap:1rem;text-align:left;padding:1rem;background:var(--white);border:1px solid var(--line);border-radius:12px}.character-choice:hover,.character-choice.is-selected{border-color:var(--coral);box-shadow:0 7px 18px rgba(227,107,85,.12)}.character-choice input{accent-color:var(--coral)}.character-choice strong{display:block}.character-choice span{display:block;color:var(--ink-soft);font-size:.88rem}.character-choice:has(input:checked){border-color:var(--coral)}
.selection-head{display:flex;justify-content:space-between;align-items:center;gap:1rem}.character-choice .character-main{flex:1;min-width:0}.character-choice .character-main>span{margin-top:.2rem}.character-choice .character-action{flex:0 0 auto;color:var(--coral);font-size:.78rem;font-weight:900;text-align:right}.character-knowledge{color:var(--ink-soft);font-size:.82rem}.character-knowledge b{color:var(--ink)}.character-card-head{display:flex;justify-content:space-between;align-items:center;gap:1rem}.character-card p{margin:.45rem 0 0}.character-card .character-knowledge{margin-top:.7rem}
.form-panel{margin-top:1.5rem;padding:1.2rem;background:var(--paper-deep);border-radius:12px}.form-panel summary{cursor:pointer;font-weight:850}.form-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.8rem;margin-top:1rem}.field{display:grid;gap:.35rem}.field label{font-size:.8rem;font-weight:800;color:var(--ink-soft)}.field input,.field textarea{width:100%;padding:.7rem .8rem;border:1px solid var(--line);border-radius:8px;background:var(--white);color:var(--ink);caret-color:var(--coral)}.field textarea{min-height:80px;resize:vertical}.form-wide{grid-column:1/-1}
.play-top{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:2rem 0 1rem}.play-top h2{margin:0;font-size:clamp(1.8rem,4vw,3.2rem);letter-spacing:-.045em}.play-top p{margin:.25rem 0 0;color:var(--ink-soft)}
 .play-grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(260px,.65fr) minmax(240px,.5fr);gap:1rem}.play-panel{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:1.25rem;box-shadow:0 8px 24px rgba(20,38,59,.06)}.play-panel h3{margin:0 0 .9rem;font-size:1rem}.scene-panel{min-height:410px;background:#eef4ef}.scene-status{display:grid;grid-template-columns:repeat(auto-fit,minmax(115px,1fr));gap:.6rem;margin:1rem 0 1.5rem}.scene-status div{padding:.75rem;background:var(--white);border-radius:9px}.scene-status span{display:block;color:var(--ink-soft);font-size:.73rem;font-weight:800}.scene-status strong{display:block;margin-top:.2rem;font-size:.95rem}.narrative{padding:1rem 1.1rem;margin:1rem 0;background:#e3eee9;border-radius:10px;font-size:1.08rem;font-weight:750}.plain-list{display:grid;gap:.55rem;margin:0;padding:0;list-style:none}.plain-list li{padding:.65rem 0;border-bottom:1px solid #d7e0dc}.plain-list li:last-child{border-bottom:0}.muted{color:var(--ink-soft)}.change-list li{font-size:.92rem}.player-panel{background:var(--ink);color:var(--white)}.player-panel .muted{color:#c6d5d5}.player-panel .plain-list li{border-color:#385269}.player-stat{padding:.8rem 0;border-bottom:1px solid #385269}.player-stat:last-child{border:0}.player-stat>span{display:block;color:#c6d5d5;font-size:.76rem}.player-stat strong{font-size:1.1rem}.player-stat .plain-list{margin-top:.25rem}.player-stat .plain-list li{padding:.28rem 0;font-size:.88rem}.action-bar{display:flex;gap:.7rem;align-items:center;margin:1rem 0 0;padding:1rem;background:var(--white);border:1px solid var(--line);border-radius:var(--radius);box-shadow:0 8px 24px rgba(20,38,59,.08)}.action-bar label{font-weight:900;white-space:nowrap}.action-input{flex:1;min-width:0;padding:.78rem .9rem;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink);caret-color:var(--coral)}.suggestions{display:flex;gap:.45rem;flex-wrap:wrap;margin-top:.7rem}.suggestion{border:1px solid var(--line);background:transparent;color:var(--ink-soft);padding:.45rem .65rem;border-radius:999px;font-size:.82rem}.suggestion:hover{border-color:var(--cobalt);color:var(--cobalt)}
.status-line{min-height:1.5rem;margin:1rem 0;color:var(--ink-soft);font-size:.9rem}.status-line.is-error{color:#9d493d}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
@media(max-width:1050px){.play-grid{grid-template-columns:1fr 1fr}.scene-panel{grid-column:1/-1}.player-panel{grid-column:2}.hero{gap:2rem}}
 @media(max-width:720px){.site-shell{padding:0 1rem 3rem}.topbar{align-items:flex-start;flex-wrap:wrap;padding:1rem 0;gap:.75rem}.main-nav{order:3;width:100%;overflow:auto}.creator-link{margin-left:auto}.hero{grid-template-columns:1fr;padding:3.5rem 0 2.5rem}.hero h1{max-width:12ch}.field-map{min-height:250px}.section-head,.shelf-head{display:block}.section-head p,.shelf-head p{margin-top:.6rem}.home-shelves{grid-template-columns:1fr;gap:2rem}.detail-layout,.play-grid{grid-template-columns:1fr}.player-panel{grid-column:auto}.detail-grid,.scene-status{grid-template-columns:repeat(2,1fr)}.form-grid{grid-template-columns:1fr}.form-wide{grid-column:auto}.continue-strip{align-items:flex-start;flex-direction:column}.session-card-head{display:block}.session-card-head .secondary-button{margin-top:.8rem}.action-bar{align-items:stretch;flex-direction:column}.action-bar label{white-space:normal}.selection-head{align-items:flex-start;flex-direction:column;gap:.2rem}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition-duration:.01ms!important;animation-duration:.01ms!important}}
"""
