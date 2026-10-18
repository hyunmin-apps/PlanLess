import Cocoa
let image = NSImage(size:NSSize(width:1024,height:1024))
image.lockFocus()
func rounded(_ r:NSRect,_ radius:CGFloat,_ color:NSColor){color.setFill();NSBezierPath(roundedRect:r,xRadius:radius,yRadius:radius).fill()}
rounded(NSRect(x:42,y:42,width:940,height:940),210,NSColor(calibratedWhite:0.10,alpha:1))
let outer=NSBezierPath(roundedRect:NSRect(x:44,y:44,width:936,height:936),xRadius:208,yRadius:208)
NSColor(white:1,alpha:0.12).setStroke();outer.lineWidth=3;outer.stroke()
rounded(NSRect(x:212,y:186,width:600,height:652),100,NSColor(calibratedWhite:0.18,alpha:1))
let outline=NSBezierPath(roundedRect:NSRect(x:212,y:186,width:600,height:652),xRadius:100,yRadius:100);NSColor(white:1,alpha:0.22).setStroke();outline.lineWidth=3;outline.stroke()
for x in [366.0,658.0]{rounded(NSRect(x:x-17,y:790,width:34,height:100),17,NSColor(calibratedWhite:0.78,alpha:1))}
rounded(NSRect(x:267,y:695,width:490,height:3),1,NSColor(white:1,alpha:0.14))
let check=NSBezierPath();check.move(to:NSPoint(x:358,y:502));check.line(to:NSPoint(x:470,y:391));check.line(to:NSPoint(x:668,y:594));check.lineWidth=49;check.lineCapStyle = .round;check.lineJoinStyle = .round;NSColor(calibratedWhite:0.94,alpha:1).setStroke();check.stroke()
let colors:[NSColor]=[NSColor(red:0.56,green:0.79,blue:0.69,alpha:1),NSColor(red:0.58,green:0.74,blue:0.94,alpha:1),NSColor(red:0.78,green:0.65,blue:0.92,alpha:1)]
for (i,c) in colors.enumerated(){rounded(NSRect(x:426+i*68,y:267,width:36,height:36),18,c)}
image.unlockFocus()
let bitmap=NSBitmapImageRep(data:image.tiffRepresentation!)!
try bitmap.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:CommandLine.arguments[1]))
