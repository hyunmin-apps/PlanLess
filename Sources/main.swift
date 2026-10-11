import Cocoa
import WebKit
import WidgetKit

final class AppDelegate: NSObject, NSApplicationDelegate, WKScriptMessageHandler, WKNavigationDelegate, NSWindowDelegate {
 var window: NSWindow!
 var web: WKWebView!
 var pendingDay: String?
 var loaded = false
 let stateURL = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0].appendingPathComponent("StudyGlass/state.json")
 func applicationDidFinishLaunching(_ notification: Notification) {
  let menu = NSMenu(); let item = NSMenuItem(); menu.addItem(item)
  let appMenu = NSMenu(); appMenu.addItem(withTitle: "Study Glass 종료", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q"); item.submenu = appMenu; NSApp.mainMenu = menu
  window = NSWindow(contentRect: NSRect(x: 180,y: 180,width: 1080,height: 760),styleMask: [.titled,.closable,.miniaturizable,.resizable,.fullSizeContentView],backing: .buffered,defer: false)
  window.appearance = NSAppearance(named: .darkAqua); window.title = "Study Glass"; window.titlebarAppearsTransparent = true; window.titleVisibility = .hidden
  window.isOpaque = false; window.backgroundColor = .clear; window.isMovableByWindowBackground = true
  window.minSize = NSSize(width: 390,height: 510); window.delegate = self
  window.setFrameAutosaveName("StudyGlassWindow")
  let effect = NSVisualEffectView(); effect.material = .hudWindow; effect.blendingMode = .behindWindow; effect.state = .active
  window.contentView = effect
  let config = WKWebViewConfiguration(); config.userContentController.add(self,name: "native")
  let preferences: [String: Bool] = ["compact": UserDefaults.standard.bool(forKey: "compact"), "desktop": UserDefaults.standard.bool(forKey: "desktop"), "pin": UserDefaults.standard.bool(forKey: "pin")]
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
 }
 func userContentController(_ userContentController: WKUserContentController,didReceive message: WKScriptMessage) {
  guard let body = message.body as? [String: Any],let action = body["action"] as? String else { return }
  if action == "save", let state = body["state"], JSONSerialization.isValidJSONObject(state) {
   do {try FileManager.default.createDirectory(at: stateURL.deletingLastPathComponent(),withIntermediateDirectories: true); let data = try JSONSerialization.data(withJSONObject: state,options: [.prettyPrinted,.sortedKeys]);try data.write(to: stateURL,options: .atomic);syncWidget()} catch {web.evaluateJavaScript("showError('저장하지 못했어요. 저장 공간을 확인해 주세요.')")}
  } else if action == "pin" {UserDefaults.standard.set(body["value"] as? Bool == true,forKey:"pin");window.level = (body["value"] as? Bool == true) ? .floating : .normal
  } else if action == "compact" {let small = body["value"] as? Bool == true; UserDefaults.standard.set(small,forKey:"compact"); var frame = window.frame; let top = frame.maxY;frame.size = small ? NSSize(width: 410,height: 720) : NSSize(width: 1080,height: 760);frame.origin.y = top-frame.height;window.setFrame(frame,display: true,animate: true)
  } else if action == "desktop" {let desktop = body["value"] as? Bool == true;UserDefaults.standard.set(desktop,forKey:"desktop");if desktop {UserDefaults.standard.set(false,forKey:"pin")};setDesktop(desktop)}
 }
 func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
  loaded = true
  syncWidget()
  if let day = pendingDay {showDay(day);pendingDay = nil} else {setDesktop(UserDefaults.standard.bool(forKey:"desktop"))}
 }
 func application(_ application: NSApplication, open urls: [URL]) {
  guard let url = urls.first, url.scheme == "studyglass", url.host == "day" else {return}
  let day = url.lastPathComponent
  guard day.range(of:"^\\d{4}-\\d{2}-\\d{2}$",options:.regularExpression) != nil else {return}
  if loaded {showDay(day)} else {pendingDay = day}
 }
 func showDay(_ day: String) {
  setDesktop(false);UserDefaults.standard.set(false,forKey:"desktop")
  window.makeKeyAndOrderFront(nil);NSApp.activate(ignoringOtherApps:true)
  web.evaluateJavaScript("selected='\(day)';start=mon(selected);expanded=false;desktop=false;document.getElementById('desktop').classList.remove('active');save();render();")
 }
 func syncWidget() {
  let folder=FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent("Library/Containers/local.studyglass.desktop.widget/Data/Documents")
  guard FileManager.default.fileExists(atPath:folder.deletingLastPathComponent().path) else {return}
  do {try FileManager.default.createDirectory(at:folder,withIntermediateDirectories:true);let data=(try? Data(contentsOf:stateURL)) ?? Data("{}".utf8);try data.write(to:folder.appendingPathComponent("study-state.json"),options:.atomic);WidgetCenter.shared.reloadAllTimelines()} catch { NSLog("Widget sync failed: %@",String(describing:error)) }
 }
 func setDesktop(_ enabled: Bool) {
  window.level = enabled ? NSWindow.Level(rawValue: Int(CGWindowLevelForKey(.desktopIconWindow))+1) : .normal
  window.collectionBehavior = enabled ? [.canJoinAllSpaces,.stationary] : []
 }
 func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {true}
}
let app = NSApplication.shared
let delegate = AppDelegate(); app.delegate = delegate; app.setActivationPolicy(.regular); app.run()
