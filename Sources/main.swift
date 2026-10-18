import Cocoa
import WebKit
import WidgetKit

final class AppDelegate: NSObject, NSApplicationDelegate, WKScriptMessageHandler, WKNavigationDelegate, NSWindowDelegate {
 var window: NSWindow!
 var web: WKWebView!
 var pendingDay: String?
 var loaded = false
 var companion:CompanionController?
 var pendingStatusChanges:[(String,Int)] = []
 var lastPointerPoint:NSPoint?
 var lastPointerTime:Double=0
 let preferencesDefaults:UserDefaults = {
  if let folder=ProcessInfo.processInfo.environment["PLANLESS_TEST_STATE_DIR"] {return UserDefaults(suiteName:"local.planless.tests."+URL(fileURLWithPath:folder).lastPathComponent)!}
  return .standard
 }()
 // Keep the original data path and bundle identity so an update retains all plans and settings.
 let stateURL:URL = {
  if let folder=ProcessInfo.processInfo.environment["PLANLESS_TEST_STATE_DIR"] {return URL(fileURLWithPath:folder).appendingPathComponent("state.json")}
  return FileManager.default.urls(for:.applicationSupportDirectory,in:.userDomainMask)[0].appendingPathComponent("StudyGlass/state.json")
 }()
 func applicationDidFinishLaunching(_ notification: Notification) {
  let menu = NSMenu(); let item = NSMenuItem(); menu.addItem(item)
  let appMenu = NSMenu(); appMenu.addItem(withTitle: "PlanLess 종료", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q"); item.submenu = appMenu
  let companionMenu=appMenu.insertItem(withTitle:"상단바 레서 보기",action:#selector(showCompanion),keyEquivalent:"l",at:0)
  companionMenu.target=self;companionMenu.keyEquivalentModifierMask=[.command,.shift]
  let editItem = NSMenuItem(); menu.addItem(editItem); let editMenu = NSMenu(title: "편집"); editItem.submenu = editMenu
  for (title, selector, key) in [("실행 취소", "undo:", "z"), ("잘라내기", "cut:", "x"), ("복사", "copy:", "c"), ("붙여넣기", "paste:", "v"), ("전체 선택", "selectAll:", "a")] {editMenu.addItem(withTitle: title, action: Selector(selector), keyEquivalent: key)}
  NSApp.mainMenu = menu
  window = NSWindow(contentRect: NSRect(x: 180,y: 180,width: 1080,height: 760),styleMask: [.titled,.closable,.miniaturizable,.resizable,.fullSizeContentView],backing: .buffered,defer: false)
  // Closing the plan keeps its window alive for menu bar actions and URLs.
  window.isReleasedWhenClosed = false
  window.appearance = NSAppearance(named: .darkAqua); window.title = "PlanLess"; window.titlebarAppearsTransparent = true; window.titleVisibility = .hidden
  window.isOpaque = false; window.backgroundColor = .clear; window.isMovableByWindowBackground = true
  window.minSize = NSSize(width: 390,height: 510); window.delegate = self
  window.setFrameAutosaveName(ProcessInfo.processInfo.environment["PLANLESS_TEST_STATE_DIR"] == nil ? "StudyGlassWindow":"PlanLessTestWindow")
  let effect = NSVisualEffectView(); effect.material = .hudWindow; effect.blendingMode = .behindWindow; effect.state = .active
  window.contentView = effect
  let config = WKWebViewConfiguration(); config.userContentController.add(self,name: "native")
  let preferences: [String: Bool] = ["compact": preferencesDefaults.bool(forKey: "compact"), "desktop": preferencesDefaults.bool(forKey: "desktop"), "pin": preferencesDefaults.bool(forKey: "pin"),"companion":preferencesDefaults.object(forKey:"mascotVisible") == nil || preferencesDefaults.bool(forKey:"mascotVisible")]
  let prefsJSON = String(data: try! JSONSerialization.data(withJSONObject: preferences), encoding: .utf8)!
  config.userContentController.addUserScript(WKUserScript(source: "window.nativePrefs = \(prefsJSON);",injectionTime: .atDocumentStart,forMainFrameOnly: true))
  let state = (try? String(contentsOf: stateURL, encoding: .utf8)) ?? "{}"
  config.userContentController.addUserScript(WKUserScript(source: "window.savedState = \(state);",injectionTime: .atDocumentStart,forMainFrameOnly: true))
  web = WKWebView(frame: .zero,configuration: config); web.navigationDelegate = self; web.setValue(false,forKey: "drawsBackground"); web.translatesAutoresizingMaskIntoConstraints = false
  effect.addSubview(web)
  NSLayoutConstraint.activate([web.leadingAnchor.constraint(equalTo: effect.leadingAnchor),web.trailingAnchor.constraint(equalTo: effect.trailingAnchor),web.topAnchor.constraint(equalTo: effect.topAnchor,constant: 30),web.bottomAnchor.constraint(equalTo: effect.bottomAnchor)])
  let url = Bundle.main.url(forResource: "index",withExtension: "html")!; web.loadFileURL(url,allowingReadAccessTo: url.deletingLastPathComponent())
  if preferences["compact"] == true {var f = window.frame; let top = f.maxY; f.size = NSSize(width:410,height:720);f.origin.y = top-f.height;window.setFrame(f,display:true)}
  if preferences["pin"] == true {window.level = .floating}
  window.makeKeyAndOrderFront(nil); NSApp.activate(ignoringOtherApps: true)
  let controller=CompanionController(defaults:preferencesDefaults);companion=controller
  controller.onSetStatus={ [weak self] id,value in self?.setGoalStatus(id,value) }
  controller.onOpen={ [weak self] in self?.showDay(CompanionController.todayKey()) }
  controller.onPreferencesChanged={ [weak self,weak controller] in
   guard let self,let controller else {return};self.syncWidget()
   if self.loaded {self.web.evaluateJavaScript("document.getElementById('companion').classList.toggle('active',\(controller.inAppVisible));")}
  }
  controller.onAnimationUpdate={ [weak self] payload in
   guard let self,self.loaded,let data=try? JSONSerialization.data(withJSONObject:payload),let json=String(data:data,encoding:.utf8) else {return}
   self.web.evaluateJavaScript("window.setCompanionPresentation?.(\(json));")
  }
  controller.onCelebrationEnded={ [weak self] in self?.syncWidget() }
  controller.onIdlePointerUpdate={ [weak self] point in
   guard let self,self.loaded,self.window.isVisible,!self.window.isMiniaturized else {return}
   let now=ProcessInfo.processInfo.systemUptime
   guard now-self.lastPointerTime>=0.08 else {return}
   let local=self.web.convert(self.window.convertPoint(fromScreen:point),from:nil)
   if let last=self.lastPointerPoint,abs(local.x-last.x)<2,abs(local.y-last.y)<2 {return}
   self.lastPointerPoint=local;self.lastPointerTime=now
   self.web.evaluateJavaScript("window.setCompanionPointer?.(\(local.x),\(local.y));")
  }
  updateCompanion((try? JSONSerialization.jsonObject(with:Data(state.utf8)) as? [String:Any]) ?? [:])

 }
 func userContentController(_ userContentController: WKUserContentController,didReceive message: WKScriptMessage) {
  guard let body = message.body as? [String: Any],let action = body["action"] as? String else { return }
  if action == "copyText", let text = body["text"] as? String {
   NSPasteboard.general.clearContents(); NSPasteboard.general.setString(text, forType: .string)
  } else if action == "save", let state = body["state"], JSONSerialization.isValidJSONObject(state) {
   do {try FileManager.default.createDirectory(at: stateURL.deletingLastPathComponent(),withIntermediateDirectories: true); let data = try JSONSerialization.data(withJSONObject: state,options: [.prettyPrinted,.sortedKeys]);try data.write(to: stateURL,options: .atomic);updateCompanion(state as? [String:Any] ?? [:]);syncWidget()} catch {web.evaluateJavaScript("showError('저장하지 못했어요. 저장 공간을 확인해 주세요.')")}
  } else if action == "pin" {preferencesDefaults.set(body["value"] as? Bool == true,forKey:"pin");window.level = (body["value"] as? Bool == true) ? .floating : .normal
  } else if action == "compact" {let small = body["value"] as? Bool == true; preferencesDefaults.set(small,forKey:"compact"); var frame = window.frame; let top = frame.maxY;frame.size = small ? NSSize(width: 410,height: 720) : NSSize(width: 1080,height: 760);frame.origin.y = top-frame.height;window.setFrame(frame,display: true,animate: true)
  } else if action == "desktop" {let desktop = body["value"] as? Bool == true;preferencesDefaults.set(desktop,forKey:"desktop");if desktop {preferencesDefaults.set(false,forKey:"pin")};setDesktop(desktop)
  } else if action == "companion" {companion?.toggleInApp()
  } else if action == "mascotCharacter",let value=body["value"] as? String {companion?.setCharacter(value)}
 }
 func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
  loaded = true
  companion?.publishPresentation()
  syncWidget()
  if let day = pendingDay {showDay(day);pendingDay = nil} else {setDesktop(preferencesDefaults.bool(forKey:"desktop"))}
  let queued=pendingStatusChanges;pendingStatusChanges=[]
  for (id,value) in queued {setGoalStatus(id,value)}
 }
 func application(_ application: NSApplication, open urls: [URL]) {
  guard let url = urls.first, ["planless","studyglass"].contains(url.scheme ?? "") else {return}
  if url.host == "goal" {
   let items=URLComponents(url:url,resolvingAgainstBaseURL:false)?.queryItems ?? []
   guard let id=items.first(where:{$0.name=="id"})?.value,!id.isEmpty,id.count<=300,
     let raw=items.first(where:{$0.name=="status"})?.value,let value=Int(raw),(0...2).contains(value) else {return}
   setGoalStatus(id,value)
   window?.makeKeyAndOrderFront(nil);NSApp.activate(ignoringOtherApps:true)
   return
  }
  guard url.host == "day" else {return}
  let day = url.lastPathComponent
  guard day.range(of:"^\\d{4}-\\d{2}-\\d{2}$",options:.regularExpression) != nil else {return}
  if loaded {showDay(day)} else {pendingDay = day}
 }
 func showDay(_ day: String) {
  guard loaded else {pendingDay=day;return}
  setDesktop(false);preferencesDefaults.set(false,forKey:"desktop")
  window.makeKeyAndOrderFront(nil);NSApp.activate(ignoringOtherApps:true)
  web.evaluateJavaScript("selected='\(day)';start=mon(selected);expanded=false;desktop=false;document.getElementById('desktop').classList.remove('active');save();render();")
 }
 func syncWidget() {
  // Isolated UI tests never write into the installed widget's container.
  guard ProcessInfo.processInfo.environment["PLANLESS_TEST_STATE_DIR"] == nil else {return}
  let folder=FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent("Library/Containers/local.studyglass.desktop.widget/Data/Documents")
  guard FileManager.default.fileExists(atPath:folder.deletingLastPathComponent().path) else {return}
  do {
   try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true)
   let original=(try? Data(contentsOf:stateURL)) ?? Data("{}".utf8)
   var state=(try? JSONSerialization.jsonObject(with:original) as? [String:Any]) ?? [:]
   state["_mascot"]=companion?.widgetMetadata() ?? ["character":"planner","mode":"idle"]
   let data=try JSONSerialization.data(withJSONObject:state)
   try data.write(to:folder.appendingPathComponent("study-state.json"),options:.atomic);WidgetCenter.shared.reloadAllTimelines()
  } catch { NSLog("Widget sync failed: %@",String(describing:error)) }
 }
 func updateCompanion(_ state:[String:Any]) {
  let planURL=Bundle.main.url(forResource:"plan",withExtension:"json")
  let plan=planURL.flatMap {try? Data(contentsOf:$0)}.flatMap {try? JSONSerialization.jsonObject(with:$0) as? [[Any]]} ?? []
  companion?.update(CompanionSnapshot.read(state,plan:plan,today:CompanionController.todayKey()))
 }
 func setGoalStatus(_ id:String,_ value:Int,completion:((Bool)->Void)? = nil) {
  guard loaded else {pendingStatusChanges.append((id,value));return}
  guard let data=try? JSONSerialization.data(withJSONObject:[id,value]),let args=String(data:data,encoding:.utf8) else {return}
  web.evaluateJavaScript("setTaskStatus.apply(null,\(args));") {result,error in
   if let error {NSLog("Companion action failed: %@",String(describing:error))}
   completion?(error == nil && result as? Bool == true)
  }
 }
 func setDesktop(_ enabled: Bool) {
  window.level = enabled ? NSWindow.Level(rawValue: Int(CGWindowLevelForKey(.desktopIconWindow))+1) : .normal
  window.collectionBehavior = enabled ? [.canJoinAllSpaces,.stationary] : []
 }
 func applicationDidBecomeActive(_ notification: Notification) {
  if loaded {web.evaluateJavaScript("refreshRollover()")}
 }
 func applicationShouldHandleReopen(_ sender:NSApplication,hasVisibleWindows flag:Bool)->Bool {showDay(CompanionController.todayKey());return true}
 @objc func showCompanion(){companion?.showPopover()}
 func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {false}
}
let app = NSApplication.shared
let delegate = AppDelegate(); app.delegate = delegate; app.setActivationPolicy(.regular); app.run()
