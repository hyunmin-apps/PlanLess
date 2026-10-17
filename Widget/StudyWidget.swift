import SwiftUI
import WidgetKit

struct Goal: Identifiable {let id: String;let subject: String;let title: String;var status:Int=0}
struct DayPlan: Identifiable {let id: String;let goals: [Goal]}
func widgetState()->[String:Any] {
 let u=URL(fileURLWithPath:NSHomeDirectory()).appendingPathComponent("Documents/study-state.json")
 guard let d=try? Data(contentsOf:u),let s=try? JSONSerialization.jsonObject(with:d) as? [String:Any] else {return [:]};return s
}
func plans(today:String = dayKey(Date())) -> [DayPlan] {
 let state=widgetState();let statuses=state["status"] as? [String:Int] ?? [:];let extras=state["extra"] as? [String:[[String:Any]]] ?? [:]

 guard let url = Bundle.main.url(forResource:"plan",withExtension:"json"),let data = try? Data(contentsOf:url),let rows = try? JSONSerialization.jsonObject(with:data) as? [[Any]] else {return []}
 var result:[DayPlan] = rows.compactMap { row in
  guard row.count == 3,let day = row[0] as? String,let goals = row[2] as? [[String]] else {return nil}
  return DayPlan(id:day,goals:goals.enumerated().map {Goal(id:"\(day)-\($0.offset)",subject:$0.element[0],title:$0.element[1],status:statuses["\(day)-\($0.offset)"] ?? 0)})
 }
 for (day,items) in extras {
  let additional=items.compactMap { i -> Goal? in guard let id=i["id"] as? String,let title=i["title"] as? String else {return nil};return Goal(id:id,subject:i["subject"] as? String ?? "할 일",title:title,status:statuses[id] ?? 0)}
  if let index=result.firstIndex(where:{$0.id==day}) {result[index]=DayPlan(id:day,goals:result[index].goals+additional)} else {result.append(DayPlan(id:day,goals:additional))}
 }
 let edits=state["edits"] as? [String:[String:String]] ?? [:]
 let deleted=state["deleted"] as? [String:Bool] ?? [:]
 let projected = result.map { day in
  DayPlan(id:day.id,goals:day.goals.filter { deleted[$0.id] != true }.map { goal in
   let edit=edits[goal.id] ?? [:]
   return Goal(id:goal.id,subject:edit["subject"] ?? goal.subject,title:edit["title"] ?? goal.title,status:goal.status)
  })
 }
 var grouped:[String:[Goal]] = [:]
 var seen=Set<String>()
 for day in projected.sorted(by:{$0.id>$1.id}) {
  for goal in day.goals {
   let date = day.id < today && goal.status == 1 ? today : day.id
   guard seen.insert(goal.id).inserted else {continue}
   grouped[date,default:[]].append(goal)
  }
 }
 return grouped.keys.sorted().map {DayPlan(id:$0,goals:grouped[$0]!)}
}
func dayKey(_ date: Date) -> String {let f=DateFormatter();f.calendar=Calendar(identifier:.gregorian);f.dateFormat="yyyy-MM-dd";return f.string(from:date)}
func subjectTint(_ subject:String) -> Color {
 let normalized=subject.precomposedStringWithCanonicalMapping.components(separatedBy:.whitespacesAndNewlines).joined().lowercased()
 let known:[String:UInt32]=["동역학":0x8ec9b0,"전자회로":0xe4c185,"확률과통계":0x95bdf0,"확통":0x95bdf0,"자료구조":0xc6a7eb,"자구알":0xc6a7eb,"차량소프트웨어":0xe9a99b,"차소웨":0xe9a99b,"할일":0xbcbcc6]
 if let rgb=known[normalized] {return Color(red:Double((rgb>>16)&255)/255,green:Double((rgb>>8)&255)/255,blue:Double(rgb&255)/255)}
 var hash:UInt32=0;for c in normalized.unicodeScalars {hash=hash &* 31 &+ c.value}
 let h=Double(hash%360)/60, chroma=(1-abs(2*0.74-1))*0.52, m=0.74-chroma/2
 let x=chroma*(1-abs(h.truncatingRemainder(dividingBy:2)-1))
 let rgb:(Double,Double,Double)
 switch Int(h) {case 0:rgb=(chroma,x,0);case 1:rgb=(x,chroma,0);case 2:rgb=(0,chroma,x);case 3:rgb=(0,x,chroma);case 4:rgb=(x,0,chroma);default:rgb=(chroma,0,x)}
 return Color(red:rgb.0+m,green:rgb.1+m,blue:rgb.2+m)
}
struct Entry: TimelineEntry {let date:Date;let days:[DayPlan];var selected:DayPlan {days.first(where:{$0.id >= dayKey(date)}) ?? DayPlan(id:dayKey(date),goals:[])}}
struct Provider: TimelineProvider {
 func placeholder(in context:Context)->Entry {Entry(date:Date(),days:plans())}
 func getSnapshot(in context:Context,completion:@escaping(Entry)->Void){completion(Entry(date:Date(),days:plans()))}
 func getTimeline(in context:Context,completion:@escaping(Timeline<Entry>)->Void){
  let now=Date(),calendar=Calendar.current
  let dates=[now]+(1...7).compactMap{calendar.date(byAdding:.day,value:$0,to:calendar.startOfDay(for:now))}
  let entries=dates.map{Entry(date:$0,days:plans(today:dayKey($0)))}
  completion(Timeline(entries:entries,policy:.atEnd))
 }
}
struct GoalRow:View {
 let goal:Goal
 var compact=false
 var body:some View {
  HStack(alignment:.top,spacing:7){
   Image(systemName:goal.status==2 ? "checkmark.square.fill" : goal.status==1 ? "square.lefthalf.filled" : "square").font(.system(size:13)).foregroundStyle(goal.status==0 ? Color.gray:subjectTint(goal.subject))
   VStack(alignment:.leading,spacing:3){
    Text(goal.subject).font(.system(size:11,weight:.semibold)).foregroundStyle(subjectTint(goal.subject))
    Text(goal.title).font(.system(size:12,weight:.medium)).strikethrough(goal.status==2).lineLimit(compact ? 1:2)
   }
  }.frame(maxWidth:.infinity,alignment:.leading)
 }
}
struct DayView: View {
 let entry:Entry
 @Environment(\.widgetFamily) var family
 var body:some View {
  VStack(alignment:.leading,spacing:10){
   HStack {Text(entry.selected.id.suffix(5).replacingOccurrences(of:"-",with:"월 ")+"일").font(.system(size:15,weight:.bold));Spacer();Image(systemName:"checklist").foregroundStyle(.secondary)}
   if entry.selected.goals.isEmpty {Text("등록된 목표 없음").foregroundStyle(.secondary)} else if family == .systemMedium {
    LazyVGrid(columns:[GridItem(.flexible()),GridItem(.flexible())],alignment:.leading,spacing:9){ForEach(Array(entry.selected.goals.prefix(4))){GoalRow(goal:$0,compact:true)}}
   } else {
    ForEach(Array(entry.selected.goals.prefix(family == .systemSmall ? 2:5))){GoalRow(goal:$0,compact:family == .systemSmall)}
   }
   if entry.selected.goals.count > (family == .systemSmall ? 2:family == .systemMedium ? 4:5) {Text("+ \(entry.selected.goals.count-(family == .systemSmall ? 2:family == .systemMedium ? 4:5))개").font(.system(size:9)).foregroundStyle(.secondary)}
   Spacer(minLength:0)
  }.frame(maxWidth:.infinity,maxHeight:.infinity,alignment:.topLeading)
  .containerBackground(Color(red:0.09,green:0.09,blue:0.10),for:.widget)
  .widgetURL(URL(string:"studyglass://day/\(entry.selected.id)"))
  .environment(\.colorScheme,.dark)
 }
}
struct WeekDayCell:View {
 let day:DayPlan
 var body:some View {
  Link(destination:URL(string:"studyglass://day/\(day.id)")!) {
   VStack(alignment:.leading,spacing:3){
    Text(day.id.suffix(5).replacingOccurrences(of:"-",with:".")).font(.system(size:11,weight:.bold)).foregroundStyle(.white)
    ForEach(day.goals){goal in
     (Text(goal.subject+" ").foregroundColor(subjectTint(goal.subject))+Text(goal.title).foregroundColor(.white)).font(.system(size:9)).lineLimit(1)
    }
   }.frame(maxWidth:.infinity,minHeight:57,alignment:.topLeading)
  }.buttonStyle(.plain)
 }
}
func weekDays(_ entry:Entry)->[DayPlan] {
 let f=DateFormatter();f.dateFormat="yyyy-MM-dd"
 guard let date=f.date(from:entry.selected.id) else {return []}
 let c=Calendar.current;let monday=c.date(byAdding:.day,value:-((c.component(.weekday,from:date)+5)%7),to:date)!
 return (0..<7).map { i in let key=dayKey(c.date(byAdding:.day,value:i,to:monday)!);return entry.days.first(where:{$0.id==key}) ?? DayPlan(id:key,goals:[]) }
}
struct WeekView:View {
 let entry:Entry
 var body:some View {
  VStack(alignment:.leading,spacing:9){
   Text("주간 계획").font(.system(size:15,weight:.bold))
   LazyVGrid(columns:[GridItem(.flexible()),GridItem(.flexible())],alignment:.leading,spacing:9){
    ForEach(weekDays(entry)){WeekDayCell(day:$0)}
   }
   Spacer(minLength:0)
  }.containerBackground(Color(red:0.09,green:0.09,blue:0.10),for:.widget).environment(\.colorScheme,.dark)
 }
}
struct StudyDayWidget:Widget {
 let kind="StudyGlassDay"
 var body:some WidgetConfiguration {StaticConfiguration(kind:kind,provider:Provider()){DayView(entry:$0)}.configurationDisplayName("하루 목표").description("과목별 공부 분량을 확인하고 앱에서 체크합니다.").supportedFamilies([.systemSmall,.systemMedium,.systemLarge])}
}
struct StudyWeekWidget:Widget {
 let kind="StudyGlassWeek"
 var body:some WidgetConfiguration {StaticConfiguration(kind:kind,provider:Provider()){WeekView(entry:$0)}.configurationDisplayName("주간 목표").description("날짜별 공부 분량을 한눈에 확인합니다.").supportedFamilies([.systemLarge])}
}
@main struct StudyWidgets:WidgetBundle {var body:some Widget {StudyDayWidget();StudyWeekWidget()}}
