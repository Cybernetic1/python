# From http://superuser.com/questions/661419/how-do-i-transfer-pdf-files-to-my-ipad-to-take-on-a-business-trip  
  
import os  
  
header = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n<plist version=\"1.0\">\n<dict>\n <key>Books</key>\n  <array>\n"  
  
footer = "  </array>\n</dict>\n</plist>"  
fst = "     <dict>\n            <key>Inserted-By-iBooks</key>\n         <false/>\n             <key>Name</key>\n            <string>"  
tnd = "</string>\n          <key>Page Progression Direction</key>\n         <string>default</string>\n          <key>Path</key>\n           <string>"  
lst = "</string>\n          <key>s</key>\n          <string>0</string>\n        </dict>\n"  
bodystr = ""  
  
for root, dirs, files in os.walk(".", topdown=False):  
    for name in files:  
        sttmp = os.path.join(root, name)[2:]  
        if not ".pdf" in sttmp:  
            continue  
        bodystr+=fst  
        bodystr+=sttmp[:-4]  
        bodystr+=tnd  
        bodystr+=sttmp  
        bodystr+=lst  
  
file = open("/home/yky/Books.plist", "w")  
file.write(header);  
file.write(bodystr);  
file.write(footer);  
file.close();  
