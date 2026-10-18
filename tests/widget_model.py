#!/usr/bin/env python3
"""Run the production widget projection with old and edited state fixtures."""
import pathlib,subprocess,tempfile,json
root=pathlib.Path(__file__).resolve().parents[1]
s=(root/'Widget/PlanLessWidget.swift').read_text()
s=s[s.index('struct Goal:'):s.index('func dayKey(')]
s=s.replace('today:String = dayKey(Date())', 'today:String = "2026-10-12"')
start=s.index('func widgetState()');end=s.index('func plans(',start)
s=s[:start]+'''func widgetState()->[String:Any] {
 let data=try! Data(contentsOf:URL(fileURLWithPath:CommandLine.arguments[2]))
 return try! JSONSerialization.jsonObject(with:data) as! [String:Any]
}
'''+s[end:]
s=s.replace('Bundle.main.url(forResource:"plan",withExtension:"json")','Optional(URL(fileURLWithPath:CommandLine.arguments[1]))')
s='import Foundation\n'+s+'''\nlet output=plans().map {day in ["id":day.id,"goals":day.goals.map {g in ["id":g.id,"subject":g.subject,"title":g.title,"status":g.status] as [String:Any]}] as [String:Any]}
print(String(data:try! JSONSerialization.data(withJSONObject:output),encoding:.utf8)!)
'''
with tempfile.TemporaryDirectory(prefix='planless-widget-test-') as d:
 p=pathlib.Path(d);(p/'main.swift').write_text(s)
 subprocess.run(['xcrun','swiftc',str(p/'main.swift'),'-o',str(p/'test')],check=True)
 (p/'plan.json').write_text(json.dumps([['2026-10-12','', [['과목','목표',''] for _ in range(4)]]]))
 fixture={'status':{'2026-10-12-0':2},'extra':{'2026-10-12':[{'id':'custom-test','subject':'기존 과목','title':'기존 목표'}]}}
 def project():
  (p/'state.json').write_text(json.dumps(fixture))
  return json.loads(subprocess.check_output([str(p/'test'),str(p/'plan.json'),str(p/'state.json')],text=True))[0]['goals']
 before=project();assert len(before)==5 and before[0]['status']==2
 fixture.update(edits={'2026-10-12-0':{'subject':'수정 과목','title':'수정 내용'},'custom-test':{'subject':'사용자 과목','title':'사용자 수정'}},deleted={'2026-10-12-1':True})
 after=project();assert len(after)==4;assert after[0]['subject']=='수정 과목' and after[0]['title']=='수정 내용' and after[0]['status']==2
 assert after[-1]['title']=='사용자 수정';assert not any(g['id']=='2026-10-12-1' for g in after)
 (p/'plan.json').write_text('[]');fixture={}
 (p/'state.json').write_text('{}')
 assert json.loads(subprocess.check_output([str(p/'test'),str(root/'Resources/plan.json'),str(p/'state.json')],text=True))==[]
 fixture={'extra':{'2026-10-10':[{'id':'move','subject':'수학','title':'진행'},{'id':'done','title':'완료'},{'id':'idle','title':'미시작'}]},'status':{'move':1,'done':2}}
 (p/'state.json').write_text(json.dumps(fixture))
 days=json.loads(subprocess.check_output([str(p/'test'),str(root/'Resources/plan.json'),str(p/'state.json')],text=True))
 assert [g['id'] for g in days[0]['goals']]==['done','idle']
 assert days[1]['id']=='2026-10-12' and days[1]['goals'][0]['id']=='move'
 print('PASS: widget legacy state, edited default/custom goals, deletion and status preservation')
