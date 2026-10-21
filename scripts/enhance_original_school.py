#!/usr/bin/env python3
"""Upgrade embedded real school scene with functioning 3D workshop exhibits and presentation."""
from pathlib import Path
s = Path("index.html").read_text(encoding="utf-8")
assert s.count('id="chemSchoolIntro"') == 1, "Original 3D scene missing"
assert "function finalSchool(" in s and "function buildFinalWorld()" in s
def change(a, b):
    global s
    count = s.count(a)
    if count != 1: raise ValueError(f"Expected exactly one occurrence ({count}): {a[:150]}")
    s = s.replace(a, b, 1)

# Keep the REAL 3D school geometry and the ORIGINAL embedded Mustafa portrait,
# but place them in the same 3D world as three moving school-workshop models.
change("const camera=new T.PerspectiveCamera(38,innerWidth/innerHeight,.02,70);",
       "const camera=new T.PerspectiveCamera(44,innerWidth/innerHeight,.02,90);")
change("camera.position.set(.82,1.28,3.38);controls.target.set(.17,.91,0);controls.update();",
       "camera.position.set(0,2.58,9.4);controls.target.set(0,1.35,-4.4);controls.update();")
change("controls.enablePan=false;controls.minDistance=1;controls.maxDistance=20;",
       "controls.enablePan=false;controls.minDistance=4;controls.maxDistance=24;")
change("const portrait=finalPerson.children[0];portrait.material.depthTest=false;portrait.renderOrder=200;",
       "const portrait=finalPerson.children[0];portrait.material.depthTest=true;portrait.renderOrder=1;")

new_position = """function positionPortrait(){
 finalPerson.visible=true;
 finalPerson.position.set(0,.012,-1.72);
 portrait.scale.set(1.35,2.1,1);
}
"""
start = s.index("function positionPortrait(){")
end = s.index("function resize(){", start)
s = s[:start] + new_position + s[end:]
change("""camera.position.set(.82+Math.sin(t*.20)*.38,1.28+Math.sin(t*.15)*.08,3.38+Math.sin(t*.27)*.35);
  controls.target.set(.17,.91,0);""",
       """camera.position.set(Math.sin(t*.12)*1.4,2.58+Math.sin(t*.13)*.12,9.4+Math.cos(t*.12)*.3);
  controls.target.set(0,1.35,-4.4);""")
change("controls.update();positionPortrait();renderer.render(finalWorld,camera);",
       "controls.update();positionPortrait();animateWorkshop((now-start)/1000);renderer.render(finalWorld,camera);")

models = r"""
// ORIGINAL biology school 3D geometry remains unchanged.
// These are new ACTUAL Three.js meshes, not CSS illustrations or photos.
const workSteel=new T.MeshStandardMaterial({color:0xbfcdd7,metalness:.69,roughness:.34});
const workShadow=new T.MeshStandardMaterial({color:0x1a3649,metalness:.53,roughness:.42});
const workBlue=new T.MeshStandardMaterial({color:0x087da2,metalness:.44,roughness:.33});
const workGold=new T.MeshStandardMaterial({color:0xe7b34c,metalness:.58,roughness:.38});
const workDark=new T.MeshStandardMaterial({color:0x23303b,metalness:.57,roughness:.37});
function workMesh(parent,geo,mat,x=0,y=0,z=0){
 const m=new T.Mesh(geo,mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
}
function workBox(parent,w,h,d,mat,x=0,y=0,z=0){return workMesh(parent,new T.BoxGeometry(w,h,d),mat,x,y,z)}
function workCylinder(parent,r,h,mat,x=0,y=0,z=0){return workMesh(parent,new T.CylinderGeometry(r,r,h,40),mat,x,y,z)}
function workStation(x,title){
 const g=new T.Group();g.position.set(x,0,-3.65);finalWorld.add(g);
 workBox(g,2.1,.14,1.52,workShadow,0,.14);
 workBox(g,2.15,.055,1.56,workSteel,0,.24);
 for(const xx of [-.9,.9])for(const zz of [-.57,.57])workBox(g,.08,.2,.08,workSteel,xx,.06,zz);
 const cn=document.createElement('canvas');cn.width=512;cn.height=96;
 const ctx=cn.getContext('2d');
 ctx.fillStyle='#052b41';ctx.fillRect(0,0,512,96);
 ctx.fillStyle='#eaffff';ctx.font='bold 34px Arial';ctx.textAlign='center';ctx.fillText(title,256,61);
 const texture=new T.CanvasTexture(cn);texture.colorSpace=T.SRGBColorSpace;
 workMesh(g,new T.PlaneGeometry(1.9,.34),new T.MeshBasicMaterial({map:texture}),0,.42,.79);
 return g;
}
function workGear(parent,x,y,r,material,teeth){
 const g=new T.Group();g.position.set(x,y,.05);parent.add(g);
 workCylinder(g,r*.82,.18,material).rotation.x=Math.PI/2;
 const ring=workMesh(g,new T.TorusGeometry(r*.76,.065,12,48),workSteel,0,0,.11);
 for(let i=0;i<teeth;i++){
  const a=2*Math.PI*i/teeth;
  const tooth=workBox(g,.15,.20,.18,material,Math.cos(a)*r,Math.sin(a)*r,.05);
  tooth.rotation.z=a;
 }
 workCylinder(g,.14,.23,workDark,0,0,.15).rotation.x=Math.PI/2;
 return g;
}
// Three technical workshops lined up side by side directly in front of school.
const mechanics=workStation(-3.1,'MAKİNE ATÖLYESİ');
const gearOne=workGear(mechanics,-.4,1.15,.57,workGold,16);
const gearTwo=workGear(mechanics,.44,1.03,.48,workSteel,12);
workBox(mechanics,.15,1.12,.18,workShadow,-.75,.93,-.23);
const piston=workBox(mechanics,.15,.56,.16,workBlue,.78,1.40,-.23);
workBox(mechanics,.43,.32,.29,workDark,.78,1.83,-.23);

const turbine=workStation(0,'UÇAK MOTOR BAKIMI');
workCylinder(turbine,.65,1.05,workSteel,0,1.18,0).rotation.x=Math.PI/2;
workCylinder(turbine,.54,1.07,workDark,0,1.18,.025).rotation.x=Math.PI/2;
workMesh(turbine,new T.TorusGeometry(.64,.09,12,54),workBlue,0,1.18,.6);
const fan=new T.Group();fan.position.set(0,1.18,.64);turbine.add(fan);
for(let i=0;i<14;i++){
 const a=i*Math.PI*2/14,blade=workBox(fan,.13,.51,.075,workSteel,Math.sin(a)*.27,Math.cos(a)*.27);
 blade.rotation.z=-a-.31;
}
workCylinder(fan,.14,.17,workGold).rotation.x=Math.PI/2;
for(const x of [-.36,.36])workBox(turbine,.16,.65,.22,workShadow,x,.67,0);
workBox(turbine,1.3,.10,.43,workSteel,0,.32);

const mechatronics=workStation(3.1,'MEKATRONİK');
workCylinder(mechatronics,.51,.20,workSteel,0,.36);
const swivel=new T.Group();swivel.position.set(0,.45,0);mechatronics.add(swivel);
workCylinder(swivel,.31,.18,workBlue,0,.1);
const arm=new T.Group();arm.position.set(0,.17,0);swivel.add(arm);
workBox(arm,.25,.99,.25,workSteel,.12,.55).rotation.z=-.22;
workCylinder(arm,.23,.21,workGold,.22,1.07).rotation.x=Math.PI/2;
workBox(arm,.23,.80,.24,workBlue,.48,1.31).rotation.z=-.67;
workBox(arm,.44,.17,.23,workSteel,.76,1.57);
workBox(arm,.09,.38,.1,workGold,.96,1.42);
workBox(arm,.09,.38,.1,workGold,.64,1.42);
function animateWorkshop(t){
 gearOne.rotation.z=t*.90;
 gearTwo.rotation.z=-t*1.1;
 fan.rotation.z=-t*4.1;
 arm.rotation.z=Math.sin(t*.74)*.17;
 swivel.rotation.y=Math.sin(t*.32)*.3;
 piston.position.y=1.40+Math.sin(t*1.1)*.17;
}
"""
change("buildFinalWorld();\nconst portrait=finalPerson.children[0];",
       "buildFinalWorld();\n"+models+"\nconst portrait=finalPerson.children[0];")

style = r"""
<style id="chem-school-workshop-style">
#chemSchoolIntro .chem-school-fade{background:linear-gradient(180deg,#051525b8,transparent 26%,transparent 60%,#051525c4)!important}
#chemSchoolIntro .chem-school-head{left:3%;right:auto;top:3%;text-align:left;max-width:550px;background:#06213bc9;border:1px solid #65c8e07a;border-radius:18px;padding:13px 20px}
#chemSchoolIntro .chem-school-head h2{font-size:clamp(26px,4vw,56px);margin:7px 0}
#chemSchoolIntro .chem-school-by{margin-top:3px;font-size:clamp(11px,1vw,14px)}
#chemSchoolIntro .chem-school-footer{bottom:4%;left:50%;right:auto;transform:translateX(-50%);justify-content:center;max-width:96vw;width:max-content}
#chemSchoolIntro .chem-school-tag{right:3%;left:auto;top:4%;font-weight:800}
#chemSchoolIntro .chem-school-orbit-hint{bottom:15%;left:3%;background:#08273fbb;border-radius:8px;padding:6px 10px}
#slideLaunch{position:fixed;top:12px;right:183px;z-index:1200;padding:10px 14px;background:#153c5b;border:1px solid #75e8f2;border-radius:10px;color:#f5ffff;font-size:13px;font-weight:850;cursor:pointer;box-shadow:0 5px 25px #0007}
#slideLaunch:hover{background:#225678}
#atomSlideShow[hidden]{display:none!important}
#atomSlideShow{position:fixed;inset:0;z-index:10000;background:#071426;color:#edfaff;font-family:system-ui,Segoe UI,Arial,sans-serif;overflow:auto}
#atomSlideShow button{font:inherit;font-weight:800;cursor:pointer;background:#164261;color:white;border:1px solid #69cddd;border-radius:10px;padding:11px 17px}
#atomSlideShow button:hover:not(:disabled){background:#23618a}
#atomSlideShow button:disabled{opacity:.35;cursor:default}
.slideHeader{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:12px 4%;background:#102743;border-bottom:1px solid #31758f}
.slideHeader strong{font-size:16px}
.slideContent{min-height:calc(100vh - 155px);padding:35px 5%;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;background:radial-gradient(circle at 50% 35%,#204c79,#0a1830 75%)}
.slideContent h2{color:#87ebf4;font-size:clamp(34px,6vw,75px);margin:15px auto}
.slideContent p{max-width:850px;line-height:1.6;font-size:clamp(18px,2.4vw,27px);color:#dce9fa}
.slideIllustration{font-size:clamp(95px,15vw,170px);filter:drop-shadow(0 0 25px #7fefff88)}
.slideFoot{color:#b6c8e0;font-size:14px;margin:20px auto}
.slideControls{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:13px;background:#102743;padding:13px}
.slideControls span{min-width:60px;text-align:center}
@media(max-width:700px){
 #chemSchoolIntro .chem-school-head{left:3%;top:3%;right:3%;max-width:none;text-align:center;padding:8px}
 #chemSchoolIntro .chem-school-head h2{font-size:26px;margin:3px}
 #chemSchoolIntro .chem-school-tag{top:auto;bottom:21%;left:3%;right:auto;font-size:10px}
 #chemSchoolIntro .chem-school-orbit-hint{display:none}
 #chemSchoolIntro .chem-school-footer{bottom:3%;width:96%;gap:5px;max-width:96%}
 #chemSchoolIntro button{font-size:11px!important;padding:10px 8px}
 #slideLaunch{top:8px;right:131px;font-size:11px;padding:8px}
 header{padding-top:57px!important}
}
</style>
"""
change("</head>", style + "</head>")
change('<select id="languagePicker" aria-label="Language / Dil">',
       '<button id="slideLaunch" type="button">▶ Slayta Git</button><select id="languagePicker" aria-label="Language / Dil">')
change('<button type="button" id="chemSchoolSkip" class="chem-school-secondary">Ana sayfa</button>',
       '<button type="button" id="chemSchoolSkip" class="chem-school-secondary">Ana sayfa</button><button type="button" id="chemSchoolSlides" class="chem-school-secondary">▶ Slayta Git</button>')
slides = r"""
<section id="atomSlideShow" role="dialog" aria-modal="true" aria-label="Kimya dönemi slayt sunumu" hidden>
 <div class="slideHeader"><strong>⚛ ATOM LAB 3D • KİMYA DÖNEM PROJESİ</strong><button id="slideExit" type="button">✕ Kapat</button></div>
 <div class="slideContent"><div id="slideNumber"></div><div class="slideIllustration" id="slidePicture"></div><h2 id="slideHeading"></h2><p id="slideParagraph"></p><div class="slideFoot" id="slideFoot"></div></div>
 <div class="slideControls"><button id="slidePrevious">← Önceki</button><span id="slideCounter"></span><button id="slideNext">Sonraki →</button><button id="slideLab">⚛ Laboratuvar</button><button id="slideMap">🗺 Türkiye Haritası</button></div>
</section>
<script id="atom-lab-slides-controller">
(()=>{
 const $=id=>document.getElementById(id);
 const slides={
 tr:[["🏫","İPOSB Pancar MTAL","Okulumuzun özgün 3D modeli, Mustafa ve önünde yan yana hareket eden makine, uçak motoru ve mekatronik modelleri.","Muhammed Mustafa Seyhan"],["⚛","Atom Nedir?","Atomlar maddenin yapı taşlarıdır. Proton ve nötronlar çekirdekte, elektronlar ise orbitallerde bulunur.","Atomun yapısı"],["🔬","Atom Modelleri","Dalton, Thomson, Rutherford ve Bohr modelleri farklı deneylerden elde edilen kanıtlarla geliştirilmiştir.","Bilimin gelişimi"],["🧪","118 Element","Periyodik tabloda her element farklı bir atom numarasına sahiptir. Atom numarası proton sayısını gösterir.","Periyodik tablo"],["🗺️","Türkiye Bilim Haritası","81 il, plaka numaraları ve 1–81 atom numaralı elementler arasında kurulan eğitim amaçlı eşleşmeleri keşfet.","81 il • 118 element"]],
 en:[["🏫","İPOSB Pancar Technical School","The original 3D school, Mustafa, and three working workshop models are shown together.","Muhammed Mustafa Seyhan"],["⚛","What Is an Atom?","Atoms are the building blocks of matter. Protons and neutrons form the nucleus, while electrons occupy orbitals.","Atomic structure"],["🔬","Atomic Models","Dalton, Thomson, Rutherford and Bohr revised models as new evidence emerged.","History of science"],["🧪","118 Elements","Every element has a unique atomic number, equal to the number of protons.","Periodic table"],["🗺️","Türkiye Science Map","Explore the 81 provinces and educational matches with elements numbered 1–81.","81 provinces"]],
 de:[["🏫","İPOSB Pancar Berufsschule","Die echte 3D-Schule, Mustafa und drei bewegliche Werkstattmodelle.","Muhammed Mustafa Seyhan"],["⚛","Was ist ein Atom?","Atome bilden Materie. Protonen und Neutronen befinden sich im Kern.","Atomaufbau"],["🔬","Atommodelle","Dalton, Thomson, Rutherford und Bohr entwickelten verschiedene Atommodelle.","Wissenschaft"],["🧪","118 Elemente","Die Ordnungszahl entspricht der Anzahl der Protonen.","Periodensystem"],["🗺️","Wissenschaftskarte der Türkei","81 Provinzen und ihre Zuordnungen zu den Elementen 1–81.","81 Provinzen"]],
 fr:[["🏫","École İPOSB Pancar","L'école originale en 3D, Mustafa et trois maquettes mécaniques animées.","Muhammed Mustafa Seyhan"],["⚛","Qu'est-ce qu'un atome ?","Les atomes composent la matière. Les protons et les neutrons se trouvent dans le noyau.","Structure atomique"],["🔬","Modèles atomiques","Dalton, Thomson, Rutherford et Bohr ont développé différents modèles.","Science"],["🧪","118 éléments","Le numéro atomique correspond au nombre de protons.","Tableau périodique"],["🗺️","Carte scientifique de Turquie","Explorez les 81 provinces et les éléments numérotés de 1 à 81.","81 provinces"]],
 ru:[["🏫","Школа İPOSB Pancar","Исходная 3D-школа, Мустафа и три действующие модели мастерских.","Muhammed Mustafa Seyhan"],["⚛","Что такое атом?","Атомы образуют материю. Протоны и нейтроны находятся в ядре.","Строение атома"],["🔬","Атомные модели","Дальтон, Томсон, Резерфорд и Бор предложили разные модели.","Наука"],["🧪","118 элементов","Атомный номер равен числу протонов.","Таблица элементов"],["🗺️","Научная карта Турции","Исследуйте 81 провинцию и элементы 1–81.","81 провинция"]],
 zh:[["🏫","İPOSB Pancar 学校","原版三维学校、Mustafa 和三个可运动的车间模型。","Muhammed Mustafa Seyhan"],["⚛","什么是原子？","原子是物质的基本组成单位。质子和中子位于原子核。","原子结构"],["🔬","原子模型","道尔顿、汤姆孙、卢瑟福和玻尔提出了不同的原子模型。","科学"],["🧪","118种元素","原子序数等于质子数。","元素周期表"],["🗺️","土耳其科学地图","探索81个省份及编号1至81的元素。","81省"]]
 };
 const labels={
 tr:["▶ Slayta Git","← Önceki","Sonraki →","✕ Kapat","⚛ Laboratuvar","🗺 Türkiye Haritası"],
 en:["▶ Go to Slides","← Previous","Next →","✕ Close","⚛ Laboratory","🗺 Türkiye Map"],
 de:["▶ Zu den Folien","← Zurück","Weiter →","✕ Schließen","⚛ Labor","🗺 Türkei-Karte"],
 fr:["▶ Voir les diapositives","← Précédent","Suivant →","✕ Fermer","⚛ Laboratoire","🗺 Carte de Turquie"],
 ru:["▶ Перейти к слайдам","← Назад","Далее →","✕ Закрыть","⚛ Лаборатория","🗺 Карта Турции"],
 zh:["▶ 查看幻灯片","← 上一页","下一页 →","✕ 关闭","⚛ 实验室","🗺 土耳其地图"]
 };
 let current=0;
 const language=()=>slides[$('languagePicker').value]?$('languagePicker').value:'tr';
 function render(){
  const l=language(),a=slides[l][current],words=labels[l];
  $('slidePicture').textContent=a[0];$('slideHeading').textContent=a[1];
  $('slideParagraph').textContent=a[2];$('slideFoot').textContent=a[3];
  $('slideNumber').textContent='ATOM LAB 3D · '+(current+1);
  $('slideCounter').textContent=(current+1)+' / '+slides[l].length;
  $('slidePrevious').disabled=current===0;
  $('slideNext').disabled=current===slides[l].length-1;
  ['slideLaunch','slidePrevious','slideNext','slideExit','slideLab','slideMap'].forEach((id,i)=>$(id).textContent=words[i]);
 }
 function open(){current=0;render();$('atomSlideShow').hidden=false;document.documentElement.style.overflow='hidden'}
 function close(){$('atomSlideShow').hidden=true;document.documentElement.style.overflow=''}
 $('slideLaunch').addEventListener('click',open);
 $('chemSchoolSlides').addEventListener('click',open);
 $('slideExit').addEventListener('click',close);
 $('slidePrevious').addEventListener('click',()=>{if(current>0)current--;render()});
 $('slideNext').addEventListener('click',()=>{if(current<slides[language()].length-1)current++;render()});
 $('slideLab').addEventListener('click',()=>{close();if($('chemSchoolIntro'))$('chemSchoolExplore').click();else $('startLab').click()});
 $('slideMap').addEventListener('click',()=>{close();if($('chemSchoolIntro'))$('chemSchoolSkip').click();$('startLab').click();setTimeout(()=>$('turkiyeMap').scrollIntoView({behavior:'smooth'}),150)});
 $('languagePicker').addEventListener('change',render);
 document.addEventListener('keydown',e=>{if($('atomSlideShow').hidden)return;if(e.key==='Escape')close();else if(e.key==='ArrowRight')$('slideNext').click();else if(e.key==='ArrowLeft')$('slidePrevious').click()});
 render();
})();
</script>
"""
change("</body>", slides+"</body>")
assert len(s)>len(Path("index-before-biology-school-intro.html").read_text(encoding="utf-8"))+2_000_000
for needed in ['id="turkiyeMap"','id="startLab"','id="languagePicker"','id="slideLaunch"','id="atomSlideShow"','const mechanics=workStation','function finalSchool(']:
 assert needed in s, needed
Path("index.html").write_text(s, encoding="utf-8")
print("Original 3D school preserved, new workshop 3D meshes and presentation installed",len(s))
