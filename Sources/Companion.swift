import Cocoa
import ImageIO

final class CompanionAssets {
 private var images: [String: NSImage] = [:]
 private var times: [String: [String: [Int]]] = [:]
 init() {
  if let url=Bundle.main.url(forResource:"animations",withExtension:"json",subdirectory:"Mascots"),
     let data=try? Data(contentsOf:url),let json=try? JSONSerialization.jsonObject(with:data) as? [String:Any] {
   times=json["characters"] as? [String:[String:[Int]]] ?? [:]
  }
 }
 func durations(_ character:String,_ mode:CompanionMode)->[Int] {
  times[character]?[mode.rawValue] ?? (mode == .complete ? [180,160,120,280,160,600]:[280,160,300,240,280,240])
 }
 func image(_ character:String,_ mode:CompanionMode,_ frame:Int)->NSImage? {
  let key="\(character)/\(mode.rawValue)/frame-\(String(format:"%02d",frame+1))"
  if let image=images[key] {return image}
  guard let url=Bundle.main.url(forResource:key,withExtension:"png",subdirectory:"Mascots"),
    let source=CGImageSourceCreateWithURL(url as CFURL,nil),let cg=CGImageSourceCreateImageAtIndex(source,0,nil) else {return nil}
  let image=NSImage(cgImage:cg,size:NSSize(width:80,height:80));images[key]=image;return image
 }
}

final class CompanionSpriteView: NSView {
 var sprite:NSImage? {didSet {if oldValue !== sprite {needsDisplay=true}}}
 private var gazeX:Double=0, gazeY:Double=0
 private var gazeColumn=1,gazeRow=1
 private var lastTurn:Double=0
 override func hitTest(_ point:NSPoint)->NSView? {nil}
 override func draw(_ dirtyRect:NSRect) {
  super.draw(dirtyRect)
  let size=min(bounds.width,bounds.height)
  NSGraphicsContext.current?.imageInterpolation = .none
  sprite?.draw(in:NSRect(x:(bounds.width-size)/2,y:(bounds.height-size)/2,width:size,height:size),
    from:.zero,operation:.sourceOver,fraction:1,respectFlipped:true,hints:[.interpolation:NSImageInterpolation.none.rawValue])
 }
 func idleFrame(at now:Double)->Int {
  guard let window else {return 4}
  let local=convert(NSPoint(x:bounds.midX,y:bounds.midY),to:nil)
  let center=window.convertToScreen(NSRect(origin:local,size:.zero)).origin
  let screen=window.screen?.frame ?? NSScreen.main?.frame ?? NSRect(x:0,y:0,width:1440,height:900)
  let mouse=NSEvent.mouseLocation
  let x=max(-1,min(1,Double(mouse.x-center.x)/max(120,Double(screen.width)*0.22)))
  let y=max(-1,min(1,Double(mouse.y-center.y)/max(100,Double(screen.height)*0.22)))
  gazeX += (x-gazeX)*0.24;gazeY += (y-gazeY)*0.24
  let column=gazeX < -0.28 ? 0:gazeX > 0.28 ? 2:abs(gazeX)<0.16 ? 1:gazeColumn
  let row=gazeY > 0.28 ? 0:gazeY < -0.28 ? 2:abs(gazeY)<0.16 ? 1:gazeRow
  // Move through connected intermediate body poses; don't snap from one
  // extreme to its opposite or chatter at a direction boundary.
  if now-lastTurn>=0.12 {
   if column != gazeColumn {gazeColumn += column>gazeColumn ? 1 : -1;lastTurn=now}
   else if row != gazeRow {gazeRow += row>gazeRow ? 1 : -1;lastTurn=now}
  }
  // Blink only in neutral, so a blink never teleports a turned head to center.
  if gazeRow==1 && gazeColumn==1 && row==1 && column==1 {
   let blink=now.truncatingRemainder(dividingBy:5.4)
   if blink<0.07 {return 9};if blink<0.16 {return 10};if blink<0.23 {return 11}
  }
  return gazeRow*3+gazeColumn
 }
}

final class CompanionCard: NSVisualEffectView {
 let sprite=CompanionSpriteView()
 let characterPicker=NSPopUpButton()
 let goalPicker=NSPopUpButton()
 let visibilityButton=NSButton(title:"",target:nil,action:nil)
 private let statusLabel=NSTextField(labelWithString:"")
 private let titleLabel=NSTextField(wrappingLabelWithString:"")
 private let startButton=NSButton(title:"진행 중",target:nil,action:nil)
 private let completeButton=NSButton(title:"완료",target:nil,action:nil)
 private let openButton=NSButton(title:"계획 열기",target:nil,action:nil)
 private var goalSignature=""
 var onCharacter:((String)->Void)?
 var onGoal:((String)->Void)?
 var onStatus:((Int)->Void)?
 var onOpen:(()->Void)?
 var onVisibility:(()->Void)?
 init() {
  super.init(frame:NSRect(x:0,y:0,width:284,height:380))
  material = .hudWindow;blendingMode = .behindWindow;state = .active
  appearance=NSAppearance(named:.darkAqua);wantsLayer=true;layer?.cornerRadius=20;layer?.masksToBounds=true
  characterPicker.addItems(withTitles:["계획단장 레서","열정 레서"])
  characterPicker.target=self;characterPicker.action=#selector(changeCharacter)
  characterPicker.setAccessibilityLabel("레서 캐릭터 선택")
  visibilityButton.target=self;visibilityButton.action=#selector(toggleVisibility);visibilityButton.controlSize = .small
  let header=NSStackView(views:[characterPicker,visibilityButton]);header.orientation = .horizontal;header.spacing=6
  statusLabel.font = .systemFont(ofSize:12,weight:.semibold);statusLabel.alignment = .center
  titleLabel.font = .systemFont(ofSize:12);titleLabel.alignment = .center;titleLabel.maximumNumberOfLines=2
  titleLabel.textColor = .secondaryLabelColor
  goalPicker.target=self;goalPicker.action=#selector(changeGoal);goalPicker.setAccessibilityLabel("레서와 함께할 목표")
  startButton.target=self;startButton.action=#selector(startGoal)
  completeButton.target=self;completeButton.action=#selector(completeGoal);completeButton.bezelStyle = .rounded
  completeButton.contentTintColor=NSColor.systemGreen
  openButton.target=self;openButton.action=#selector(openPlan);openButton.controlSize = .small
  let actions=NSStackView(views:[startButton,completeButton]);actions.orientation = .horizontal;actions.distribution = .fillEqually;actions.spacing=8
  let stack=NSStackView(views:[header,sprite,statusLabel,titleLabel,goalPicker,actions,openButton]);stack.orientation = .vertical;stack.alignment = .centerX;stack.spacing=7
  stack.translatesAutoresizingMaskIntoConstraints=false;addSubview(stack)
  NSLayoutConstraint.activate([
   stack.leadingAnchor.constraint(equalTo:leadingAnchor,constant:14),stack.trailingAnchor.constraint(equalTo:trailingAnchor,constant:-14),
   stack.topAnchor.constraint(equalTo:topAnchor,constant:14),stack.bottomAnchor.constraint(lessThanOrEqualTo:bottomAnchor,constant:-12),
   header.widthAnchor.constraint(equalTo:stack.widthAnchor),sprite.widthAnchor.constraint(equalToConstant:144),sprite.heightAnchor.constraint(equalToConstant:144),
   goalPicker.widthAnchor.constraint(equalTo:stack.widthAnchor),actions.widthAnchor.constraint(equalTo:stack.widthAnchor),titleLabel.widthAnchor.constraint(equalTo:stack.widthAnchor),titleLabel.heightAnchor.constraint(equalToConstant:32)])
 }
 required init?(coder:NSCoder) {fatalError("init(coder:) is not supported")}
 @objc private func changeCharacter(){onCharacter?(characterPicker.indexOfSelectedItem==1 ? "passion":"planner")}
 @objc private func changeGoal(){if let id=goalPicker.selectedItem?.representedObject as? String {onGoal?(id)}}
 @objc private func startGoal(){onStatus?(1)}
 @objc private func completeGoal(){onStatus?(2)}
 @objc private func openPlan(){onOpen?()}
 @objc private func toggleVisibility(){onVisibility?()}
 func update(character:String,goals:[CompanionGoal],selectedID:String?,presentation:CompanionPresentation,inAppVisible:Bool) {
  let index=character=="passion" ? 1:0
  if characterPicker.indexOfSelectedItem != index {characterPicker.selectItem(at:index)}
  visibilityButton.title=inAppVisible ? "앱에서 숨기기":"앱에 표시"
  visibilityButton.setAccessibilityLabel(inAppVisible ? "앱 안의 레서 숨기기":"앱 안의 레서 표시")
  let signature=goals.map {"\($0.id):\($0.status):\($0.title)"}.joined(separator:"|")
  if goalSignature != signature {
   goalSignature=signature;goalPicker.removeAllItems()
   for goal in goals {
    goalPicker.addItem(withTitle:"\(goal.status==1 ? "◐":"○") \(goal.day.suffix(5)) · \(goal.title.prefix(28))")
    goalPicker.lastItem?.representedObject=goal.id
   }
   if goals.isEmpty {goalPicker.addItem(withTitle:"진행할 목표 없음")}
  }
  if let id=selectedID,let item=goalPicker.itemArray.first(where:{$0.representedObject as? String == id}) {goalPicker.select(item)}
  let selected=goals.first(where:{$0.id==selectedID})
  titleLabel.stringValue=selected.map {"\($0.subject) · \($0.title)"} ?? "계획을 추가하고 함께 시작해 보세요."
  startButton.isEnabled=selected != nil && selected?.status != 1
  completeButton.isEnabled=selected != nil
  goalPicker.isEnabled = !goals.isEmpty
  switch presentation.mode {
  case .idle:statusLabel.stringValue="쉬는 중 · 눈과 고개가 따라봐요"
  case .working:statusLabel.stringValue="진행 중 · \(goals.filter{$0.status==1}.count)개"
  case .complete:statusLabel.stringValue="잘했어요! · 축하 \(presentation.celebrationNumber) / 5"
  }
 }
}

final class CompanionController:NSObject {
 let playback=CompanionPlayback()
 let assets=CompanionAssets()
 let popoverCard=CompanionCard()
 private let defaults:UserDefaults
 private let statusItem=NSStatusBar.system.statusItem(withLength:34)
 private let barSprite=CompanionSpriteView()
 private let popover=NSPopover()
 private var timer:Timer?
 private var observers:[NSObjectProtocol]=[]
 private var selectedGoalID:String?
 private var displayedGoals:[CompanionGoal]=[]
 private var lastMode:CompanionMode = .idle
 private var presentationSignature=""
 private var cardSignature=""
 var onAnimationUpdate:(([String:Any])->Void)?
 var onIdlePointerUpdate:((NSPoint)->Void)?
 var onSetStatus:((String,Int)->Void)?
 var onOpen:(()->Void)?
 var onPreferencesChanged:(()->Void)?
 var onCelebrationEnded:(()->Void)?
 var character:String {defaults.string(forKey:"mascotCharacter")=="passion" ? "passion":"planner"}
 var inAppVisible:Bool {defaults.object(forKey:"mascotVisible") == nil || defaults.bool(forKey:"mascotVisible")}
 init(defaults:UserDefaults) {
  self.defaults=defaults
  super.init()
  let vc=NSViewController();vc.view=popoverCard;popover.contentViewController=vc;popover.contentSize=NSSize(width:284,height:380);popover.behavior = .transient
  if let button=statusItem.button {
   button.target=self;button.action=#selector(statusClicked(_:));button.sendAction(on:[.leftMouseUp,.rightMouseUp])
   barSprite.frame=button.bounds;barSprite.autoresizingMask=[.width,.height];button.addSubview(barSprite)
   button.setAccessibilityLabel("PlanLess 레서");button.toolTip="PlanLess · 레서와 계획 보기"
  }
  for card in [popoverCard] {
   card.onCharacter={ [weak self] c in self?.setCharacter(c) }
   card.onGoal={ [weak self] id in self?.selectedGoalID=id;self?.tick() }
   card.onStatus={ [weak self] status in guard let self,let id=self.selectedGoalID else {return};self.onSetStatus?(id,status) }
   card.onOpen={ [weak self] in self?.popover.performClose(nil);self?.onOpen?() }
   card.onVisibility={ [weak self] in self?.toggleInApp() }
  }
  startTimer()
  let nc=NSWorkspace.shared.notificationCenter
  observers.append(nc.addObserver(forName:NSWorkspace.willSleepNotification,object:nil,queue:.main){[weak self] _ in self?.timer?.invalidate();self?.timer=nil})
  observers.append(nc.addObserver(forName:NSWorkspace.didWakeNotification,object:nil,queue:.main){[weak self] _ in self?.startTimer()})
 }
 deinit {timer?.invalidate();for observer in observers {NSWorkspace.shared.notificationCenter.removeObserver(observer)}}
 private func startTimer() {
  timer?.invalidate()
  let t=Timer(timeInterval:1.0/24,repeats:true){[weak self] _ in self?.tick()};t.tolerance=0.008
  RunLoop.main.add(t,forMode:.common);timer=t;tick()
 }
 func update(_ snapshot:CompanionSnapshot) {
  playback.update(snapshot,at:ProcessInfo.processInfo.systemUptime)
  cardSignature=""
  let today=Self.todayKey()
  displayedGoals=snapshot.goals.filter {$0.status != 2 && ($0.status==1 || $0.day>=today)}
  let goals=availableGoals
  if !goals.contains(where:{$0.id==selectedGoalID}) {selectedGoalID=goals.first?.id}
  lastMode=playback.presentation(at:ProcessInfo.processInfo.systemUptime).mode
  tick()
 }
 private var availableGoals:[CompanionGoal] {
  displayedGoals
 }
 static func todayKey()->String {
  let f=DateFormatter();f.calendar=Calendar(identifier:.gregorian);f.locale=Locale(identifier:"en_US_POSIX");f.dateFormat="yyyy-MM-dd";return f.string(from:Date())
 }
 func widgetMetadata()->[String:Any] {
  let p=playback.presentation(at:ProcessInfo.processInfo.systemUptime)
  // WidgetKit receives a representative still and one expiry entry, not a
  // battery-heavy artificial stream of animation timelines.
  let remaining=p.mode == .complete ? max(0,7.5*Double(playback.queue.count)-p.elapsed):0
  return ["character":character,"mode":p.mode.rawValue,"completionUntil":remaining>0 ? Date().timeIntervalSince1970+remaining:0]
 }
 @objc private func statusClicked(_ sender:Any?) {
  if NSApp.currentEvent?.type == .rightMouseUp {showMenu();return}
  if popover.isShown {popover.performClose(nil)} else {showPopover()}
 }
 func showPopover() {
  guard let button=statusItem.button else {return}
  tick();popover.show(relativeTo:button.bounds,of:button,preferredEdge:.minY)
 }
 private func showMenu() {
  let menu=NSMenu()
  for (title,action) in [("계획 열기",#selector(openPlan)),(inAppVisible ? "앱 안의 레서 숨기기":"앱 안의 레서 표시",#selector(toggleInAppAction))] {
   let item=menu.addItem(withTitle:title,action:action,keyEquivalent:"");item.target=self
  }
  menu.addItem(.separator())
  for (i,title) in ["계획단장 레서","열정 레서"].enumerated() {
   let item=menu.addItem(withTitle:title,action:#selector(selectCharacter(_:)),keyEquivalent:"");item.target=self;item.tag=i;item.state=(character==(i==0 ? "planner":"passion")) ? .on:.off
  }
  menu.addItem(.separator());menu.addItem(withTitle:"PlanLess 종료",action:#selector(NSApplication.terminate(_:)),keyEquivalent:"q")
  if let button=statusItem.button {menu.popUp(positioning:nil,at:NSPoint(x:0,y:button.bounds.minY),in:button)}
 }
 @objc private func openPlan(){onOpen?()}
 @objc private func toggleInAppAction(){toggleInApp()}
 @objc private func selectCharacter(_ sender:NSMenuItem){setCharacter(sender.tag==1 ? "passion":"planner")}
 func toggleInApp() {
  let value = !inAppVisible;defaults.set(value,forKey:"mascotVisible")
  onPreferencesChanged?();publishPresentation()
 }
 func setCharacter(_ value:String) {
  defaults.set(value=="passion" ? "passion":"planner",forKey:"mascotCharacter")
  onPreferencesChanged?();publishPresentation()
 }
 func publishPresentation() {presentationSignature="";tick()}
 private func tick() {
  let now=ProcessInfo.processInfo.systemUptime,p=playback.presentation(at:now),c=character
  if p.mode == .idle && inAppVisible {onIdlePointerUpdate?(NSEvent.mouseLocation)}
  if p.mode != lastMode {
   let ended=lastMode == .complete;lastMode=p.mode
   if ended {onCelebrationEnded?()}
  }
  for view in [barSprite,popoverCard.sprite] {
   if view === popoverCard.sprite && !popover.isShown {continue}
   let frame=p.mode == .idle ? view.idleFrame(at:now):CompanionPlayback.frame(at:p.elapsed,milliseconds:assets.durations(c,p.mode))
   view.sprite=assets.image(c,p.mode,frame)
  }
  let signature="\(c):\(p.mode.rawValue):\(p.celebrationNumber):\(inAppVisible)"
  let cardKey=signature+":"+(selectedGoalID ?? "")
  if cardSignature != cardKey {
   cardSignature=cardKey
   popoverCard.update(character:c,goals:availableGoals,selectedID:selectedGoalID,presentation:p,inAppVisible:inAppVisible)
  }
  if signature != presentationSignature {
   presentationSignature=signature
   onAnimationUpdate?(["character":c,"mode":p.mode.rawValue,"elapsedMs":p.elapsed*1000,"celebrationNumber":p.celebrationNumber,"visible":inAppVisible])
   statusItem.button?.setAccessibilityLabel("PlanLess 레서 · \(p.mode == .complete ? "완료 축하 \(p.celebrationNumber)/5":p.mode == .working ? "진행 중":"대기")")
  }
 }
}
