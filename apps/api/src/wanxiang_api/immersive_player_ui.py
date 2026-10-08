"""Opt-in experimental spatial Player; illustrative meshes are NOT world truth.

This route is intentionally separate from R7 and the v5.5 stable experience.
The Babylon dependency is version-pinned CDN for prototype only, not production.
"""

# ruff: noqa: E501  # Inline HTML/CSS/JS resource (same pattern as Player UI assets).

IMMERSIVE_PLAYER_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#101d29">
<title>万相 · 江南机关城 · 空间体验实验场</title>
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#111e29;color:#eef6f1;font-family:"Microsoft YaHei","Noto Sans SC",sans-serif}button,input{font:inherit}
#scene{position:fixed;inset:0;width:100%;height:100%;touch-action:none;display:block;outline:none}
.layer{position:fixed;z-index:3;border:1px solid #ffffff30;background:rgba(9,25,37,.78);backdrop-filter:blur(12px);box-shadow:0 16px 45px #081c2570;border-radius:14px}
.top{top:16px;left:18px;right:18px;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:12px 18px}
.brand{font-size:21px;font-weight:900;letter-spacing:.08em}.subtitle{font-size:12px;color:#c6d8dc;margin-top:3px}
.top a{color:#f0efde;text-decoration:none;padding:7px 12px;border:1px solid #8cb7b882;border-radius:7px}
.card{left:18px;bottom:22px;width:min(420px,calc(100vw - 36px));padding:18px}
.card h1{font-size:17px;margin:0 0 10px}.card p{margin:8px 0;color:#d8e5e3;font-size:14px;line-height:1.6}
#note{min-height:26px;color:#f0bd86}#world-facts{font-size:13px;line-height:1.65}
.right{right:18px;top:105px;width:min(320px,calc(100vw - 36px));padding:13px 15px}
.right h2{font-size:15px;margin:0 0 9px}.right p{font-size:13px;line-height:1.5;margin:7px 0;color:#c8dbd9}
.row{display:flex;gap:7px;flex-wrap:wrap;margin:8px 0}
button{cursor:pointer;border:1px solid #90b6b6;padding:10px 12px;border-radius:8px;background:#153d46;color:#f5f6eb;font-weight:700}
button:hover,button:focus-visible{outline:2px solid #f1ba7c;outline-offset:2px}button:disabled{opacity:.45}
input{flex:1;min-width:130px;padding:10px;border:1px solid #a3c9c3;border-radius:8px;background:#e7eee9;color:#1b3335}
.warning{background:#72503a;border-radius:8px;padding:9px;font-size:12px;color:#fff4e8}
#fallback{position:fixed;inset:0;z-index:1;display:none;background:linear-gradient(180deg,#a7cad1 0%,#a9c8aa 35%,#416d72 35%,#234858 80%,#142b37)}
#fallback svg{width:100%;height:100%;opacity:.88}
#frame-status{position:fixed;top:90px;left:23px;z-index:5;font-size:12px;color:#eddbc3}
@media(max-width:720px){.top{left:7px;right:7px;top:7px;padding:8px 10px}.brand{font-size:16px}.subtitle{font-size:10px}.right{top:80px;right:7px;width:155px;padding:9px}.card{left:7px;bottom:7px;width:calc(100vw - 14px);padding:10px}.right p{font-size:11px}.card p{font-size:12px}.card h1{font-size:14px}button{padding:8px 9px}.top a{font-size:12px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
</style>
</head>
<body>
<canvas id="scene" aria-label="可拖动旋转与缩放的江南机关城实验三维沙盘"></canvas>
<div id="fallback" aria-label="三维图形不可用时的二维场景示意">
<svg viewBox="0 0 1000 680" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="水道、拱桥、城楼和河岸民居">
<defs><linearGradient id="river" x2="0" y2="1"><stop stop-color="#4e989c"/><stop offset="1" stop-color="#1e5773"/></linearGradient></defs>
<path d="M0 430L1000 120v240L0 670Z" fill="url(#river)"/>
<path d="M0 405L1000 92" stroke="#bca986" stroke-width="25"/>
<path d="M0 680L1000 362" stroke="#a99880" stroke-width="35"/>
<g fill="#efe3c6" stroke="#6c5a4b" stroke-width="5"><path d="M130 240h170v130H130z"/><path d="M620 370h170v140H620z"/><path d="M420 70h180v120H420z"/></g>
<g fill="#304b57"><path d="M110 245l100-80 110 80Z"/><path d="M600 375l110-85 100 85Z"/><path d="M400 75l100-75 120 75Z"/></g>
<path d="M400 460Q500 250 620 390" fill="none" stroke="#d8c6a5" stroke-width="40"/>
<text x="40" y="75" fill="#fff9e8" font-size="42" font-weight="bold">江南机关城 · 场景示意</text>
</svg></div>
<div class="layer top">
<div><div class="brand">万相 · 江南机关城</div><div class="subtitle">一个可以进入、观看与改变的持久世界 · 早期三维体验实验</div></div>
<a href="/" aria-label="返回原有玩家世界入口">返回世界广场</a>
</div>
<div id="frame-status" role="status" aria-live="polite">正在核验世界观察数据…</div>
<aside class="layer right">
<h2>视角与世界</h2>
<div class="row"><button id="orbit">俯瞰沙盘</button><button id="walk">进入街巷</button></div>
<p>鼠标拖动旋转、滚轮缩放；街巷视角使用 WASD 与鼠标。点击建筑查看实验场景标记。</p>
<p id="world-facts">尚未连接世界</p>
<p class="warning">这是原创程序几何搭建的<b>示意场景</b>，不是从 Canonical World 推导的精确街区、NPC 位置或建筑事实。</p>
</aside>
<section class="layer card">
<h1 id="place">潮汐门初启 · 沉水巷</h1>
<p id="selection">选中城门、桥梁、水轮或街道可查看标记。示意对象本身不表示可提交的 World Action。</p>
<p id="note" role="status"></p>
<form id="act-form"><div class="row"><input id="intent" aria-label="向真实世界提交角色行动" placeholder="输入角色行动，例如：让自己保持清醒"><button id="send" type="submit">提交世界行动</button></div></form>
<p>只有服务器确认并返回新的 World Observation，才显示“世界发生变化”。</p>
</section>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babylonjs/7.54.3/babylon.js"></script>
<script>
(function(){
"use strict";
const B=window.BABYLON, canvas=document.getElementById("scene"), notice=document.getElementById("frame-status");
const facts=document.getElementById("world-facts"), note=document.getElementById("note"), label=document.getElementById("place");
const selection=document.getElementById("selection"), intent=document.getElementById("intent");
const id=new URLSearchParams(location.search).get("instance_id");
let worldView=null,engine=null,scene=null,orbit=null,walk=null,light=null,water=null,mode="orbit";
const headers={"content-type":"application/json","x-wanxiang-user":"studio","x-wanxiang-locale":"zh-CN"};
function showError(s){notice.textContent=s;note.textContent=s}
function showView(v){
  worldView=v;
  const name=String(v.world&&v.world.name||"未知世界");
  facts.textContent="世界："+name+"　角色："+String(v.player&&v.player.name||"未知")+"　世界时刻："+String((v.time&&v.time.ticks)||0)+"　天气："+String(v.weather||"未记录");
  const change=v.recent_changes&&v.recent_changes[0];
  label.textContent=String(v.location||"场景位置尚未记录")+" · "+String(v.region||"江南机关城");
  if(change&&change.summary){note.textContent="服务器世界后果："+String(change.summary)}
  if(light){const phase=Number(v.time&&v.time.ticks||0)%24;light.intensity=phase>=18||phase<6?0.55:1.1}
  if(water){water.material.alpha=0.88}
}
async function request(path,options){
  const r=await fetch(path,Object.assign({headers:headers},options||{}));
  const body=await r.json().catch(()=>({}));
  if(!r.ok)throw Error("世界服务返回 "+r.status+": "+String(body.detail||"操作失败"));
  return body;
}
function material(name,color,alpha){
  const m=new B.StandardMaterial(name,scene);m.diffuseColor=B.Color3.FromHexString(color);m.specularColor=new B.Color3(.07,.09,.1);if(alpha!==undefined)m.alpha=alpha;return m;
}
function mesh(kind,name,size,pos,mat,tag){
  let m;if(kind==="box")m=B.MeshBuilder.CreateBox(name,{width:size[0],height:size[1],depth:size[2]},scene);
  else if(kind==="cylinder")m=B.MeshBuilder.CreateCylinder(name,{diameter:size[0],height:size[1],tessellation:10},scene);
  else m=B.MeshBuilder.CreateSphere(name,{diameter:size[0],segments:10},scene);
  m.position=new B.Vector3(pos[0],pos[1],pos[2]);m.material=mat;
  if(tag){m.metadata={landmark:tag};m.isPickable=true}else m.isPickable=false;
  return m;
}
function scenery(){
  const grass=material("moss","#607e5e"),stone=material("road","#b7ab91"),wall=material("plaster","#e5d5ba"),roof=material("roof","#405b66"),timber=material("timber","#6c4a3c"),river=material("river","#387f91",.88),leaf=material("leaf","#5b885f"),bronze=material("bronze","#aa8051"),red=material("red","#945b4e");
  mesh("box","island",[96,.45,72],[0,-.25,0],grass);
  water=mesh("box","canal",[100,.10,13],[0,.025,0],river,"河道 · 视觉示意");
  mesh("box","north road",[100,.1,5],[0,.10,-10],stone,"沉水巷 · 美术示意");
  mesh("box","south road",[100,.1,5],[0,.10,10],stone);
  for(const x of [-33,0,33]){
    mesh("box","bridge",[8,.7,17],[x,.8,0],stone,"机关桥 · 美术示意");
    mesh("box","rail a",[8,.9,.7],[x,1.6,-7.6],timber);
    mesh("box","rail b",[8,.9,.7],[x,1.6,7.6],timber);
  }
  for(let i=0;i<25;i++){
    const x=-42+(i%9)*10;
    const z=(i%3===0?-24:(i%3===1?24:30));
    const height=4+(i%3)*1.25;
    mesh("box","house",[5.6,height,5.6],[x,height/2,z],wall,"民居与作坊 · 程序几何示意");
    const top=mesh("box","tile roof",[7,.8,7],[x,height+.35,z],roof);top.rotation.z=(i%2===0?.09:-.09);
    mesh("box","door",[1.2,2,.14],[x,height*.25,z-2.87],timber);
    if(i%4===0)mesh("box","banner",[.65,2,.15],[x+2.2,height+1.3,z-2],red);
  }
  for(const x of [-23,22]){
    for(const z of [-15,16,34]){
      mesh("cylinder","trunk",[.75,3,0],[x,1.5,z],timber);
      mesh("sphere","crown",[4,4,0],[x,4.3,z],leaf);
    }
  }
  mesh("box","wall north",[94,5,2],[0,2.5,-37],stone);
  mesh("box","wall west",[2,5,76],[-48,2.5,0],stone);
  mesh("box","wall east",[2,5,76],[48,2.5,0],stone);
  mesh("box","tower body",[15,10,10],[0,5,-35],wall,"潮汐门 · 美术示意");
  mesh("box","tower roof",[19,1.1,14],[0,11,-35],roof);
  mesh("box","tower opening",[5,5,.25],[0,2.4,-29.9],timber);
  const wheel=mesh("cylinder","waterwheel",[5,1,0],[18,2.8,3.5],bronze,"水轮机关 · 美术示意");wheel.rotation.x=Math.PI/2;
  mesh("box","workshop",[10,7,8],[24,3.5,17],wall,"机关作坊 · 美术示意");
  mesh("box","workshop roof",[12,1,10],[24,7.5,17],roof);
  scene.onPointerObservable.add(function(info){
    if(info.type!==B.PointerEventTypes.POINTERPICK)return;
    const picked=info.pickInfo&&info.pickInfo.pickedMesh;
    if(picked&&picked.metadata&&picked.metadata.landmark){
      selection.textContent= picked.metadata.landmark+"。该空间标记尚未与经过验证的 WorldSceneManifest 绑定；不能据此宣称世界事实或提交位移。";
    }
  });
}
function init(){
  if(!B){document.getElementById("fallback").style.display="block";showError("3D 引擎加载失败；当前显示二维示意场景。请检查网络和图形环境。");return}
  try{
    engine=new B.Engine(canvas,true,{preserveDrawingBuffer:true,stencil:true});
    scene=new B.Scene(engine);scene.clearColor=new B.Color4(.60,.76,.78,1);
    orbit=new B.ArcRotateCamera("overview",Math.PI*.75,1.06,89,new B.Vector3(0,0,0),scene);orbit.lowerRadiusLimit=12;orbit.upperRadiusLimit=120;orbit.attachControl(canvas,true);
    walk=new B.UniversalCamera("immersive",new B.Vector3(-5,2.2,17),scene);walk.speed=.5;walk.angularSensibility=3000;walk.keysUp=[87];walk.keysDown=[83];walk.keysLeft=[65];walk.keysRight=[68];
    light=new B.HemisphericLight("ambient",new B.Vector3(0,1,0),scene);light.intensity=1.1;
    const sun=new B.DirectionalLight("sun",new B.Vector3(-.3,-1,.5),scene);sun.intensity=.7;
    scenery();
    scene.activeCamera=orbit;
    engine.runRenderLoop(function(){scene.render()});
    window.addEventListener("resize",function(){engine.resize()});
    document.getElementById("orbit").onclick=function(){walk.detachControl(canvas);scene.activeCamera=orbit;orbit.attachControl(canvas,true);mode="orbit";note.textContent="已切换至俯瞰沙盘；镜头移动属于本地视觉状态。"};
    document.getElementById("walk").onclick=function(){orbit.detachControl(canvas);scene.activeCamera=walk;walk.attachControl(canvas,true);mode="walk";note.textContent="已进入街巷镜头；WASD 只移动本地摄像机，不会修改世界中角色的位置。"};
    notice.textContent="3D 实验场已加载；正在读取世界观察…";
    if(worldView)showView(worldView);
  }catch(e){document.getElementById("fallback").style.display="block";showError("WebGL 不可用，已回退二维场景："+String(e.message||e))}
}
async function start(){
  init();
  if(!id){showError("缺少实例 ID：必须从真实 Player 进入，不会伪造世界会话。");document.getElementById("send").disabled=true;return}
  try{
    const result=await request("/experience/player/instances/"+encodeURIComponent(id));
    if(String(result.view&&result.view.world&&result.view.world.name)!=="江南机关城"){showError("此世界暂未制作专属空间场景。不能使用江南机关城图像冒充其他世界。");document.getElementById("send").disabled=true;return}
    showView(result.view);notice.textContent="已关联真实 Player 世界观察 · 本地画面布局为示意";
  }catch(e){showError("无法读取真实世界："+String(e.message));document.getElementById("send").disabled=true}
}
document.getElementById("act-form").addEventListener("submit",async function(event){
  event.preventDefault();if(!id||!worldView)return;
  const text=intent.value.trim();if(!text)return;
  const submit=document.getElementById("send");submit.disabled=true;note.textContent="正在请求世界 Authority；尚未确认发生变化。";
  try{
    const result=await request("/experience/player/instances/"+encodeURIComponent(id)+"/action",{method:"POST",body:JSON.stringify({text:text})});
    showView(result.view);
    note.textContent=result.changed?"已获得服务器确认的世界变化；详细后果见纪事。":"服务器未确认世界变化；不能展示伪造后果。";
    intent.value="";
  }catch(e){showError("世界行动未完成："+String(e.message))}
  finally{submit.disabled=false}
});
start();
})();
</script>
</body></html>"""


def immersive_player_html() -> str:
    """Return an explicitly experimental world-visualization surface."""
    return IMMERSIVE_PLAYER_HTML
