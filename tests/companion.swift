import Foundation

@main struct CompanionChecks {
 static func goal(_ id:String,_ status:Int)->CompanionGoal {
  CompanionGoal(id:id,day:"2026-10-18",subject:"과목",title:id,status:status)
 }
 static func main() {
  let player=CompanionPlayback()
  func update(_ goals:[CompanionGoal],_ now:Double){player.update(CompanionSnapshot(goals:goals),at:now)}
  update([goal("a",2),goal("b",0)],0)
  assert(player.presentation(at:0).mode == .idle,"Historical completions must not replay on launch")
  update([goal("a",2),goal("b",1),goal("c",1)],10)
  assert(player.presentation(at:10).mode == .working)
  update([goal("a",2),goal("b",2),goal("c",1)],11)
  for loop in 0..<5 {
   let p=player.presentation(at:11+Double(loop)*1.5+0.01)
   assert(p.mode == .complete && p.celebrationNumber == loop+1)
  }
  assert(player.presentation(at:18.499).mode == .complete)
  assert(player.presentation(at:18.5).mode == .working,"After exactly 5 loops, another in-progress goal keeps working")
  update([goal("a",2),goal("b",2),goal("c",2)],20)
  update([goal("a",2),goal("b",2),goal("c",2)],21)
  assert(player.queue.count==1,"Repeated saves cannot extend/replay completion")
  assert(player.presentation(at:27.5).mode == .idle)
  let queue=CompanionPlayback()
  queue.update(CompanionSnapshot(goals:[goal("a",1),goal("b",1)]),at:0)
  queue.update(CompanionSnapshot(goals:[goal("a",2),goal("b",1)]),at:1)
  queue.update(CompanionSnapshot(goals:[goal("a",2),goal("b",2)]),at:2)
  assert(queue.queue==["a","b"])
  assert(queue.presentation(at:8.5).mode == .complete && queue.queue==["b"])
  assert(queue.presentation(at:16).mode == .idle,"Rapid completions each get their own five loops")
  queue.update(CompanionSnapshot(goals:[goal("a",1),goal("b",0)]),at:17)
  queue.update(CompanionSnapshot(goals:[goal("a",2),goal("b",0)]),at:18)
  queue.update(CompanionSnapshot(goals:[goal("a",1),goal("b",0)]),at:19)
  assert(queue.presentation(at:19).mode == .working,"Undo cancels the undone celebration")
  let state:[String:Any]=["status":["old":1,"deleted":1,"ghost":1,"done":2],"deleted":["deleted":true],
   "extra":["2026-10-17":[["id":"old","title":"원래 제목"],["id":"deleted","title":"삭제"]],"2026-10-18":[["id":"done","title":"완료"]]],
   "edits":["old":["subject":"수정 과목","title":"수정 제목"]]]
  let projected=CompanionSnapshot.read(state,plan:[],today:"2026-10-18")
  assert(projected.goals.count==2 && projected.hasWork)
  assert(projected.goals[0].id=="old" && projected.goals[0].day=="2026-10-18" && projected.goals[0].title=="수정 제목")
  let times=[180,160,120,280,160,600]
  assert(CompanionPlayback.frame(at:0,milliseconds:times)==0)
  assert(CompanionPlayback.frame(at:0.18,milliseconds:times)==1)
  assert(CompanionPlayback.frame(at:1.499,milliseconds:times)==5)
  assert(CompanionPlayback.frame(at:1.5,milliseconds:times)==0)
  print("PASS: five completion loops, remaining work, idle fallback, repeated saves, rapid completion queue, undo, projection, frame boundaries")
 }
}
