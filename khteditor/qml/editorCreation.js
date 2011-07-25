var component;
var editor;
var editorsArray = new Array();
var newPageCounter = 0;
var filePath = '';

function createEditorObject(newPageCounter) {
    console.log('createEditorObject called');
    filePath = '';
    component = Qt.createComponent("EditorItem.qml");
    if (component.status == Component.Ready)
        finishCreation();
    else
        component.statusChanged.connect(finishCreation);
    return component;
}

function openEditorObject(filepath) {
    console.log('createEditorObject called')
    filePath = filepath ;
    component = Qt.createComponent("EditorItem.qml");
    if (component.status == Component.Ready)
        finishCreation();
    else
        component.statusChanged.connect(finishCreation);
    return component;
}

function switchEditor(filepath) {
    console.log('switchEditor called')
    var len=editorsArray.length;
    for(var i=0; i<len; i++) {
            if (editorsArray[i].hasOwnProperty("filepath"))
            {
                if (editorsArray[i].filepath === filepath)
                {
                    editors.currentTab = editorsArray[i]
                    return
                }
            }
    }
}


function modificationChanged(filepath, filename) {
    console.log('modificationChanged called')
    var len=editorsArray.length;
    for(var i=0; i<len; i++) {
            if (editorsArray[i].hasOwnProperty("filepath"))
            {
                if (editorsArray[i].filepath === filepath)
                {
                    editorsModel.set(i,{'filename':filename})
                    return
                }
            }
    }
}

function closeEditor(filepath) {
    console.log('closeEditor called')
    var len=editorsArray.length;
    for(var i=0; i<len; i++) {
            if (editorsArray[i].hasOwnProperty("filepath"))
            {
                if (editorsArray[i].filepath === filepath)
                {
                    editorsArray[i].destroy();
                    editorsModel.remove(i);
                    editorsArray.splice(1,i);
                    if (i<len){
                        editors.currentTab = editorsArray[i];
                    }
                    else {
                        if (i>0) {
                        editors.currentTab = editorsArray[i-1];
                        }
                    }
                    return
                }
            }
    }
}


function finishCreation() {
    if (component.status == Component.Ready) {
        editor = component.createObject(editors);
        if (editor === null) {
            // Error Handling
            console.log("Error creating object");}
        else{
//            editor.modificationChanged.connect(finishCreation);
            if (filePath == '') {
                newPageCounter = newPageCounter + 1;
                editor.filename = 'Untitled ' + newPageCounter;
                editor.filepath = editor.filename;
                //editor.isNewFile = true;
            }
            else {
                //editor.isNewFile = false;
                editor.loadFile(filePath);
               // editor.filepath = filePath
            }
            editors.currentTab = editor;
            editorsArray.push(editor)
            editorsModel.append({'filepath':editor.filepath,'filename':editor.filename})
            console.log("Editor object created");
        }
    } else if (component.status == Component.Error) {
        // Error Handling
        console.log("Error loading component:", component.errorString());
    }
}

