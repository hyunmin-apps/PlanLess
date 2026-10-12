/* Shared by the app and import validation tests. No network requests. */
(function(root){
function parse(text){
 if(text.length>1000000)throw Error('계획은 1MB 이하로 나눠 붙여넣어 주세요.');
 const clean=text.trim().replace(/^```(?:json)?\s*\n?([\s\S]*?)\n?```$/i,'$1');
 let value;try{value=JSON.parse(clean)}catch{throw Error('JSON 양식을 확인해 주세요. AI 응답의 JSON 전체를 붙여넣어 주세요.')}
 if(!value||value.version!==1||!Array.isArray(value.tasks)||!value.tasks.length)throw Error('version: 1과 비어 있지 않은 tasks 배열이 필요해요.');
 if(value.tasks.length>500)throw Error('한 번에 최대 500개까지 등록할 수 있어요.');
 return value.tasks.map((t,i)=>{
 const fail=s=>{throw Error(`${i+1}번째 할 일: ${s}`)};
 if(!t||typeof t!=='object')fail('할 일 형식을 확인해 주세요.');
 if(typeof t.date!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(t.date)||t.date<'2000-01-01'||t.date>'2100-12-31')fail('날짜는 2000~2100년의 YYYY-MM-DD 형식이어야 해요.');
 const date=new Date(t.date+'T12:00:00Z');if(!Number.isFinite(date.getTime())||date.toISOString().slice(0,10)!==t.date)fail('존재하지 않는 날짜예요.');
 const result={date:t.date};
 for(const [field,max,label] of [['subject',30,'과목명'],['title',180,'할 일'],['detail',3000,'세부 내용']]){
 const v=t[field]??(field==='detail'?'':null);
 if(typeof v!=='string'||(field!=='detail'&&!v.trim()))fail(`${label}을 입력해 주세요.`);
 if(v.trim().length>max)fail(`${label}은 ${max}자 이하여야 해요.`);
 result[field]=v.trim().normalize('NFC');
 }
 return result;
 });
}
const signature=t=>JSON.stringify([t.subject.normalize('NFC').trim(),t.title.normalize('NFC').trim(),(t.detail||'').normalize('NFC').trim()]);
function prepare(rows,tasksForDate){
 const seen=new Map();let skipped=0;
 const tasks=rows.filter(t=>{
 if(!seen.has(t.date))seen.set(t.date,new Set(tasksForDate(t.date).map(signature)));
 const set=seen.get(t.date),id=signature(t);if(set.has(id)){skipped++;return false}set.add(id);return true;
 }).sort((a,b)=>a.date.localeCompare(b.date));
 return {tasks,skipped};
}
root.PlanImport={parse,prepare};
})(typeof module==='object'?module.exports:globalThis);
