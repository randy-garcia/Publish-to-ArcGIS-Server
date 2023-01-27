import arcpy
import os
from tkinter import filedialog
from tkinter import *
from tkinter import ttk


def printtext():
    global serviceNameEntry
    global mapNameEntry
    serviceName = serviceNameEntry.get() 
    mapName = mapNameEntry.get()
    #print (serviceName + mapName)   

def selectServer():
    global serverFile
    global pathFile
    serverFile = filedialog.askopenfilename(initialdir = "os.path.expanduser('~\Documents\ArcGIS')",title = "Select file",filetypes = (("AGS files","*.ags"),("all files","*.*")))
    pathFile = os.path.dirname(serverFile)
    print(serverFile)
    cb1 = StringVar()
    cb1.set("\u263A")
    cb1label=Label(root, textvariable=cb1, height=2)
    cb1label.grid(column=2, row=3)
    #print(pathFile)
    #print(serverFile)

def selectAprx():
    global aprxFile
    global dataFrames
    aprxFile = filedialog.askopenfilename(initialdir = "os.path.expanduser('~\Documents\ArcGIS')",title = "Select file",filetypes = (("APRX Files","*.aprx"),("all files","*.*")))
    print(aprxFile)
    cb2 = StringVar()
    cb2.set("\u263A")
    cb2label=Label(root, textvariable=cb2, height=2)
    cb2label.grid(column=2, row=1)
    dataFrames = []
    aprxFile = arcpy.mp.ArcGISProject(aprxFile)
    for m in aprxFile.listMaps():
        dataFrames.append(m.name)
    #print (dataFrames)
    mapNameLabel = StringVar()
    mapNameLabel.set("Name of ArcGIS Pro Data Frame")
    labelmap=Label(root, textvariable=mapNameLabel, height=2)
    labelmap.grid(column=0, row=2)
    combotext = StringVar()
    combotext.set('Select Data Frame')

    box = ttk.Combobox(root, textvariable=combotext, state='readonly')
    box['values'] = dataFrames

    def callback_function(event):
        global dataFrameName
        dataFrameName = combotext.get()
        #print('You selected:', combotext.get())
        #print(dataFrameName)

    root.bind('<<ComboboxSelected>>', callback_function)
    box.grid(column=1, row=2)
    

def popupmsg():
    popup = Tk()
    popup.wm_title("!")
    be = Button(popup, text='ArcGIS Service Succesfully Published',command=quit)
    be.grid(column=1, row=2)
    popup.mainloop()

def quit():
    global popup
    popup.quit()

def createService():
    global serviceNameEntry
    print ("starting Operation...")
    serviceName = serviceNameEntry.get()
    #mapName = mapNameEntry.get()
    mapName = dataFrameName
    #print (mapName)
    #outdir = r"C:\Project\Output"
    outdir = pathFile
    service = serviceName
    #print(service)
    sddraft_filename = service + ".sddraft"
    sddraft_output_filename = os.path.join(outdir, sddraft_filename)

    # Reference map to publish
    aprx = aprxFile
    #print (aprxFile)
    m = aprx.listMaps(mapName)[0]

    # Create MapServiceDraft and set service properties
    service_draft = arcpy.sharing.CreateSharingDraft("STANDALONE_SERVER", "MAP_SERVICE", service, m)
    service_draft.targetServer = serverFile

    # Create Service Definition Draft file
    service_draft.exportToSDDraft(sddraft_output_filename)

    # Stage Service
    sd_filename = service + ".sd"
    sd_output_filename = os.path.join(outdir, sd_filename)
    arcpy.StageService_server(sddraft_output_filename, sd_output_filename)

    # Share to portal
    print("Uploading Service Definition...")
    arcpy.UploadServiceDefinition_server(sd_output_filename, serverFile)
    print("Successfully Uploaded service.")

root = Tk()

root.geometry("400x200")
root.title('Publish to ArcGIS Server')

serviceNameLabel = StringVar()
serviceNameLabel.set("Name of Service (No spaces)")
labelDir=Label(root, textvariable=serviceNameLabel, height=2)

#mapNameLabel = StringVar()
#mapNameLabel.set("Name of ArcGIS Pro Data Frame")
#labelmap=Label(root, textvariable=mapNameLabel, height=2)

serverLabel = StringVar()
serverLabel.set("Select Server Connection File")
labelServer=Label(root, textvariable=serverLabel, height=2)

aprxLabel = StringVar()
aprxLabel.set("Select ArcGIS Pro Project")
labelaprx=Label(root, textvariable=aprxLabel, height=1)

serviceNameEntry = Entry(root)
serviceNameEntry.focus_set()


b3 = Button(root,text='Browse .ags',command=selectServer)
b4 = Button(root,text='Browse .aprx',command=selectAprx)
b2 = Button(root,text='Publish to ArcGIS Server',command=createService, bg="#76EE00",font='bold')
#b3 = Button(root,text='testToast',command=popupmsg)



#define grid
labelDir.grid(column=0, row=0)
#labelmap.grid(column=0, row=3)
labelaprx.grid(column=0, row=1)
labelServer.grid(column=0, row=3)
serviceNameEntry.grid(column=1, row=0)
b3.grid(column=1, row=3)
b4.grid(column=1, row=1)
b2.grid(column=1, row=4)



root.mainloop()
