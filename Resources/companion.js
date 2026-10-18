(function(){
 'use strict';
 const area=document.getElementById('companionArea'),canvas=document.getElementById('companionCanvas'),ctx=canvas.getContext('2d');
 const label=document.getElementById('companionStatus'),hint=document.getElementById('companionHint'),profile=document.getElementById('companionProfile'),picker=document.getElementById('companionGoal');
 let presentation={character:'planner',mode:'idle',elapsedMs:0,celebrationNumber:0,visible:window.nativePrefs?.companion!==false};
 let anchor=performance.now(),images={},timings={},ready=false,lastDraw='',pointer={x:0,y:0},smooth={x:0,y:0};
 let gazeCol=1,gazeRow=1,lastTurn=0;
 const names={planner:'계획단장 레서',passion:'열정 레서'};
 window.setCompanionPresentation=value=>{presentation={...presentation,...value};anchor=performance.now();area.hidden=!presentation.visible;profile.value=presentation.character;lastDraw='';updateLabels()};
 function updateLabels(){
  const mode=presentation.mode;
  label.textContent=mode==='complete'?`잘했어요! · 축하 ${presentation.celebrationNumber} / 5`:mode==='working'?'함께 진행 중':'쉬는 중';
  hint.textContent=mode==='complete'?'다섯 번 축하한 뒤 다음 상태로 돌아가요.':mode==='working'?'진행 중인 목표가 있는 동안 계속 응원해요.':'포인터를 움직이면 눈과 고개로 따라봐요.';
  canvas.setAttribute('aria-label',names[presentation.character]+' · '+label.textContent);
 }
 window.refreshCompanionGoals=()=>{
  if(typeof state==='undefined')return;
  const days=[...new Set([...Object.keys(state.extra||{}),...PLAN.map(p=>p[0])])].sort();
  const goals=days.flatMap(day=>tasks(day).map(t=>({...t,day,status:state.status[t.id]||0}))).filter(t=>t.status!==2);
  goals.sort((a,b)=>(b.status===1)-(a.status===1)||a.day.localeCompare(b.day));
  const old=picker.value;picker.replaceChildren();
  for(const goal of goals){const option=document.createElement('option');option.value=goal.id;option.textContent=`${goal.status===1?'◐':'○'} ${goal.title}`;picker.append(option)}
  if(goals.some(g=>g.id===old))picker.value=old;
  if(!goals.length){const option=document.createElement('option');option.textContent='진행할 목표 없음';picker.append(option)}
  picker.disabled=!goals.length;document.getElementById('companionStart').disabled=!goals.length;document.getElementById('companionComplete').disabled=!goals.length;
 };
 window.setCompanionPointer=(x,y)=>{const rect=canvas.getBoundingClientRect();pointer={x:Math.max(-1,Math.min(1,(x-rect.left-rect.width/2)/220)),y:Math.max(-1,Math.min(1,(y-rect.top-rect.height/2)/180))}};
 document.addEventListener('mousemove',event=>window.setCompanionPointer(event.clientX,event.clientY));
 document.addEventListener('mousedown',event=>window.setCompanionPointer(event.clientX,event.clientY));
 profile.onchange=()=>native('mascotCharacter',{value:profile.value});
 document.getElementById('companionStart').onclick=()=>setTaskStatus(picker.value,1);
 document.getElementById('companionComplete').onclick=()=>setTaskStatus(picker.value,2);
 function frameAt(time,times){let pos=Math.max(0,time)%times.reduce((a,b)=>a+b,0);for(let i=0;i<times.length;i++){if(pos<times[i])return i;pos-=times[i]}return 0}
 function render(now){
  if(ready&&!area.hidden&&!document.hidden){
   const c=presentation.character,mode=presentation.mode;let frame;
   if(mode==='idle'){
    smooth.x+=(pointer.x-smooth.x)*.15;smooth.y+=(pointer.y-smooth.y)*.15;
    const col=smooth.x<-.28?0:smooth.x>.28?2:Math.abs(smooth.x)<.16?1:gazeCol,row=smooth.y<-.28?0:smooth.y>.28?2:Math.abs(smooth.y)<.16?1:gazeRow;
    if(now-lastTurn>=120){if(col!==gazeCol){gazeCol+=Math.sign(col-gazeCol);lastTurn=now}else if(row!==gazeRow){gazeRow+=Math.sign(row-gazeRow);lastTurn=now}}
    frame=gazeRow*3+gazeCol;
    const blink=now%5400;if(frame===4&&col===1&&row===1&&blink<230)frame=blink<70?9:blink<160?10:11;
   }else frame=frameAt(presentation.elapsedMs+now-anchor,timings[c][mode]);
   const signature=c+'/'+mode+'/'+frame;
   if(lastDraw!==signature){lastDraw=signature;ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,80,80);ctx.drawImage(images[signature],0,0,80,80)}
  }
  requestAnimationFrame(render);
 }
 Promise.resolve({characters:window.MASCOT_TIMINGS}).then(async data=>{
  timings=data.characters;const pending=[];
  for(const c of Object.keys(timings))for(const mode of ['idle','working','complete'])for(let i=0;i<timings[c][mode].length;i++)pending.push(new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{images[c+'/'+mode+'/'+i]=im;resolve()};im.onerror=reject;im.src=`Mascots/${c}/${mode}/frame-${String(i+1).padStart(2,'0')}.png`}));
  await Promise.all(pending);ready=true;
 }).catch(()=>{hint.textContent='캐릭터를 불러오지 못했어요. 앱을 다시 열어 주세요.'});
 area.hidden=!presentation.visible;updateLabels();window.refreshCompanionGoals();requestAnimationFrame(render);
})();
