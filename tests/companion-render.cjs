const fs=require('fs'),vm=require('vm'),assert=require('assert');
const timings=JSON.parse(fs.readFileSync('Resources/Mascots/animations.json')).characters;
let tick,drawn='',now=0;
const elements={};
for(const id of ['companionArea','companionCanvas','companionStatus','companionHint','companionProfile','companionGoal','companionStart','companionComplete']) elements[id]={value:'',hidden:false,textContent:'',setAttribute(){},replaceChildren(){},append(){},getBoundingClientRect:()=>({left:100,top:100,width:144,height:144})};
elements.companionCanvas.getContext=()=>({clearRect(){},drawImage(im){drawn=im.src}});
const context={window:{MASCOT_TIMINGS:timings},document:{hidden:false,getElementById:id=>elements[id],addEventListener(){},createElement:()=>({})},state:{extra:{},status:{}},PLAN:[],tasks:()=>[],native(){},setTaskStatus(){},performance:{now:()=>now},requestAnimationFrame:f=>tick=f,Image:class{set src(v){this._src=v;this.onload()}get src(){return this._src}}};
vm.createContext(context);vm.runInContext(fs.readFileSync('Resources/companion.js','utf8'),context);
(async()=>{
 await new Promise(setImmediate);
 function step(t){now=t;tick(t)}
 context.window.setCompanionPresentation({character:'passion',mode:'idle',visible:true});
 context.window.setCompanionPointer(-1000,172);
 for(let t=1000;t<=3000;t+=20)step(t);
 assert(drawn.endsWith('passion/idle/frame-04.png'),'Left pointer must reach the complete left body pose');
 context.window.setCompanionPointer(2000,172);
 for(let t=3020;t<=5000;t+=20)step(t);
 assert(drawn.endsWith('passion/idle/frame-06.png'),'Opposite pointer must pass center and reach right pose');
 context.window.setCompanionPresentation({character:'planner',mode:'complete',elapsedMs:0,celebrationNumber:1});
 step(5000);assert(drawn.endsWith('planner/complete/frame-01.png'));
 step(5180);assert(drawn.endsWith('planner/complete/frame-02.png'));
 step(6500);assert(drawn.endsWith('planner/complete/frame-01.png'),'Variable duration animation loops at 1.5s');
 context.window.setCompanionPresentation({mode:'working',elapsedMs:0});step(6500);
 assert(drawn.includes('planner/working/'));
 context.window.setCompanionPresentation({visible:false});const before=drawn;step(7500);assert(drawn===before);
 assert(elements.companionComplete.disabled,'Empty plan must not complete a phantom task');
 console.log('PASS: production canvas loads local assets, follows global left/right pointer, switches profile/state, honors timings, hides, disables empty goals');
})().catch(error=>{console.error(error);process.exitCode=1});
