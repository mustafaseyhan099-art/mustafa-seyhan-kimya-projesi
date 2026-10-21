#!/usr/bin/env python3
"""Add the real biology school's procedural 3D scene to the chemistry homepage."""
from pathlib import Path
import re
import urllib.request

base = Path("index.html")
current = base.read_text(encoding="utf-8")
if "id=\"chemSchoolIntro\"" in current:
    print("School intro already present; no changes made.")
    raise SystemExit(0)

bio_url = "https://raw.githubusercontent.com/mustafaseyhan099-art/Mustafa-seyhan-biyoloji-projesi/main/index.html"
with urllib.request.urlopen(bio_url, timeout=45) as response:
    biology = response.read().decode("utf-8")

# This exact bundled three.js engine and school/portrait model come from the
# user's own biology site. Both are embedded into the chemistry HTML.
engine_match = re.search(r'<script>(/\* The MIT License[\s\S]*?)</script>', biology)
if not engine_match:
    raise RuntimeError("Could not find biology 3D library; refusing to change site")
engine = engine_match.group(1)
if "Biology3D" not in engine or "OrbitControls" not in engine:
    raise RuntimeError("Unexpected 3D library format")
start = biology.index("// Existing 3D school, with the approved 2D portrait")
end = biology.index("function finalWords()", start)
school = biology[start:end]
if "function finalSchool(" not in school or "function buildFinalWorld()" not in school:
    raise RuntimeError("School source missing")
if "data:image/png;base64," not in school:
    raise RuntimeError("Mustafa portrait not embedded in original scene")

style = r"""
<style id="chem-school-intro-css">
#chemSchoolIntro{position:fixed;inset:0;z-index:2147482000;overflow:hidden;background:#09182a;color:#fff;font-family:system-ui,Segoe UI,Arial,sans-serif}
#chemSchoolCanvas{position:absolute!important;inset:0;width:100%!important;height:100%!important;z-index:0;display:block;cursor:grab}
#chemSchoolIntro .chem-school-fade{position:absolute;inset:0;background:linear-gradient(90deg,transparent 36%,rgba(6,17,36,.24) 62%,rgba(5,18,37,.82)),linear-gradient(0deg,rgba(7,18,34,.88),transparent 43%);pointer-events:none;z-index:1}
#chemSchoolIntro .chem-school-head{position:absolute;z-index:3;top:6%;right:5%;text-align:right;max-width:min(550px,55vw);text-shadow:0 2px 20px #081a38}
#chemSchoolIntro .chem-school-eyebrow{font-size:clamp(11px,1.1vw,15px);font-weight:750;letter-spacing:.22em;color:#9feef5}
#chemSchoolIntro h2{font-size:clamp(36px,6.5vw,91px);letter-spacing:-.07em;line-height:.98;margin:18px 0 15px;color:#fff;font-weight:900}
#chemSchoolIntro h2 span{color:#75e8f3}
#chemSchoolIntro .chem-school-lead{font-size:clamp(14px,1.65vw,22px);font-weight:700;margin:8px 0;color:#e9f7ff}
#chemSchoolIntro .chem-school-by{font-size:clamp(12px,1.35vw,18px);color:#c9e0f1;line-height:1.45;margin-top:16px}
#chemSchoolIntro .chem-school-by strong{display:block;color:white;font-size:1.14em}
#chemSchoolIntro .chem-school-footer{position:absolute;z-index:3;right:5%;bottom:7%;display:flex;justify-content:flex-end;align-items:center;gap:12px;flex-wrap:wrap;max-width:70vw}
#chemSchoolIntro button{font-family:inherit;font-size:15px!important;font-weight:800;border-radius:13px;padding:14px 20px;cursor:pointer;color:#071c32;background:linear-gradient(130deg,#77eced,#bdf7ea);border:1px solid #aaf4f8;box-shadow:0 10px 35px #0006;transition:transform .18s,box-shadow .18s}
#chemSchoolIntro button:hover{transform:translateY(-3px);box-shadow:0 12px 30px #69e7ff44}
#chemSchoolIntro button.chem-school-secondary{background:#102b46dd;color:#ecfaff;border-color:#6aa3b7}
#chemSchoolIntro .chem-school-tag{position:absolute;left:3.5%;top:4%;z-index:3;color:#dcf4fa;background:#0b2840bd;border:1px solid #7cbfd055;padding:9px 15px;border-radius:30px;font-size:13px;letter-spacing:.04em}
#chemSchoolIntro .chem-school-orbit-hint{position:absolute;bottom:3%;left:3.5%;z-index:3;color:#e3eef2;font-size:12px;text-shadow:0 2px 7px #07172a}
@media(max-width:700px){
 #chemSchoolIntro .chem-school-fade{background:linear-gradient(0deg,rgba(5,15,31,.96) 0%,rgba(5,15,31,.18) 63%,transparent)}
 #chemSchoolIntro .chem-school-head{top:auto;bottom:21%;left:7%;right:7%;max-width:none;text-align:center}
 #chemSchoolIntro .chem-school-head h2{font-size:clamp(35px,11vw,60px);margin:7px 0}
 #chemSchoolIntro .chem-school-footer{left:7%;right:7%;bottom:6%;max-width:none;justify-content:center}
 #chemSchoolIntro button{font-size:12px!important;padding:12px}
 #chemSchoolIntro .chem-school-tag{font-size:11px;top:3%}
 #chemSchoolIntro .chem-school-orbit-hint{display:none}
}
</style>
"""
markup = r"""
<div id="chemSchoolIntro" role="region" aria-label="ATOM LAB 3D kimya projesi giriş sahnesi">
 <canvas id="chemSchoolCanvas" aria-label="İPOSB okulunun 3D sahnesi"></canvas>
 <div class="chem-school-fade"></div>
 <div class="chem-school-tag">🏫 İPOSB PANCAR MTAL · KİMYA PROJESİ</div>
 <div class="chem-school-head">
  <div class="chem-school-eyebrow">BİLİMİN YOLCULUĞUNA HOŞ GELDİNİZ</div>
  <h2>ATOM <span>LAB 3D</span></h2>
  <p class="chem-school-lead">KİMYA DÖNEM PROJESİ</p>
  <p class="chem-school-by"><strong>MUHAMMED MUSTAFA SEYHAN</strong>İPOSB PANCAR Mesleki ve Teknik Anadolu Lisesi</p>
 </div>
 <div class="chem-school-footer">
  <button type="button" id="chemSchoolExplore">⚛ Kimya laboratuvarına gir →</button>
  <button type="button" id="chemSchoolElements" class="chem-school-secondary">118 Element</button>
  <button type="button" id="chemSchoolSkip" class="chem-school-secondary">Ana sayfa</button>
 </div>
 <div class="chem-school-orbit-hint">↔ Fareyle döndür · Tekerlekle yaklaş</div>
</div>
"""
runtime = r"""
<script type="module" id="chem-school-intro-3d">
const {T,OrbitControls}=globalThis.Biology3D;
const intro=document.getElementById('chemSchoolIntro');
const canvas=document.getElementById('chemSchoolCanvas');
const renderer=new T.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.5));
renderer.outputColorSpace=T.SRGBColorSpace;
renderer.toneMapping=T.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.22;
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=T.PCFSoftShadowMap;
renderer.shadowMap.autoUpdate=false;
renderer.shadowMap.needsUpdate=true;
const camera=new T.PerspectiveCamera(38,innerWidth/innerHeight,.02,70);
const controls=new OrbitControls(camera,canvas);
controls.enableDamping=true;controls.dampingFactor=.065;
controls.enablePan=false;controls.minDistance=1;controls.maxDistance=20;
controls.minPolarAngle=.35;controls.maxPolarAngle=1.6;
camera.position.set(.82,1.28,3.38);controls.target.set(.17,.91,0);controls.update();
let staticDirty=true;
SCHOOL_MODEL_CODE
buildFinalWorld();
const portrait=finalPerson.children[0];portrait.material.depthTest=false;portrait.renderOrder=200;
let active=true,autoTour=true,raf=0,lastFrame=0;
canvas.addEventListener('pointerdown',()=>{autoTour=false},{passive:true});
canvas.addEventListener('wheel',()=>{autoTour=false},{passive:true});
function positionPortrait(){
 const fwd=controls.target.clone().sub(camera.position).normalize();
 const right=new T.Vector3().crossVectors(fwd,new T.Vector3(0,1,0)).normalize();
 const up=new T.Vector3().crossVectors(right,fwd).normalize();
 const d=4.7, halfH=Math.tan(T.MathUtils.degToRad(camera.fov/2))*d,halfW=halfH*camera.aspect;
 finalPerson.visible=true;
 finalPerson.position.copy(camera.position).addScaledVector(fwd,d)
  .addScaledVector(right,-halfW*(innerWidth<700?.36:.57))
  .addScaledVector(up,-halfH*.91);
 portrait.scale.set(1.20,1.80,1);
}
function resize(){
 if(!active)return;
 renderer.setSize(innerWidth,innerHeight,false);
 camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();
}
addEventListener('resize',resize);resize();
const start=performance.now();
function tick(now){
 if(!active)return;
 raf=requestAnimationFrame(tick);
 if(now-lastFrame<27)return;
 lastFrame=now;
 if(autoTour){
  const t=(now-start)/1000;
  camera.position.set(.82+Math.sin(t*.20)*.38,1.28+Math.sin(t*.15)*.08,3.38+Math.sin(t*.27)*.35);
  controls.target.set(.17,.91,0);
 }
 controls.update();positionPortrait();renderer.render(finalWorld,camera);
}
raf=requestAnimationFrame(tick);
function finish(which){
 active=false;cancelAnimationFrame(raf);removeEventListener('resize',resize);
 controls.dispose();
 intro.remove();
 if(which==='lab')document.getElementById('startLab')?.click();
 if(which==='elements')document.getElementById('startElements')?.click();
 if(which==='home')document.body.classList.add('home-mode');
}
document.getElementById('chemSchoolExplore').addEventListener('click',()=>finish('lab'));
document.getElementById('chemSchoolElements').addEventListener('click',()=>finish('elements'));
document.getElementById('chemSchoolSkip').addEventListener('click',()=>finish('home'));
if(location.hash==='#lab')finish('lab');
if(location.hash==='#home')finish('home');
</script>
"""
runtime = runtime.replace("SCHOOL_MODEL_CODE", school)
# The source library is entirely local, as is the school, portrait and flag art.
intro_scripts = "<script id=\"chem-school-bundled-three\">" + engine + "</script>\n" + runtime
if len(school) < 10000 or len(engine) < 100000:
    raise RuntimeError("3D scene extraction unexpectedly short")
if current.count("</head>")!=1 or current.count("</body>")!=1:
    raise RuntimeError("Unexpected chemistry page structure")
current = current.replace("</head>", style + "</head>", 1)
current = re.sub(r"(<body[^>]*>)", lambda m: m.group(1)+markup, current, count=1)
current = current.replace("</body>", intro_scripts+"\n</body>", 1)
assert current.count("id=\"chemSchoolIntro\"") == 1
assert "KİMYA DÖNEM PROJESİ" in current and "function buildFinalWorld()" in current
assert "data:image/png;base64," in current
assert "id=\"turkiyeMap\"" in current and "id=\"startLab\"" in current
assert "id=\"chemSchoolExplore\"" in current
Path("index-before-biology-school-intro.html").write_text(base.read_text(encoding="utf-8"),encoding="utf-8")
base.write_text(current,encoding="utf-8")
print("Source scene:", len(school), "3D engine:", len(engine), "merged chemistry:",len(current),"characters")
