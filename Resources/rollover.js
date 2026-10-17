(function(root){
function rollover(state,today){
 const extra=state.extra||{},status=state.status||{},deleted=state.deleted||{};
 let changed=false;const present=new Set((extra[today]||[]).map(t=>t.id));
 for(const date of Object.keys(extra).sort()){
  if(!/^\d{4}-\d{2}-\d{2}$/.test(date)||date>=today)continue;
  extra[date]=extra[date].filter(task=>{
   if(status[task.id]!==1||deleted[task.id])return true;
   if(!present.has(task.id)){(extra[today]||=[]).push(task);present.add(task.id)}
   changed=true;return false;
  });
 }
 return changed;
}
root.StudyRollover=rollover;
})(typeof module==='object'?module.exports:globalThis);
