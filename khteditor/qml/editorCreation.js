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
    var index = getModelIndexForFilepath(filepath)
    if (index < 0) {
        component = Qt.createComponent("EditorItem.qml");
        if (component.status == Component.Ready)
            finishCreation();
        else
            component.statusChanged.connect(finishCreation);
        return component;
    } else {
        switchEditor(filepath)
    }    
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
    var index = getModelIndexForFilepath(filepath)
    for(var i=0; i<len; i++) {
            if (editorsArray[i].hasOwnProperty("filepath"))
            {
                if (editorsArray[i].filepath === filepath)
                {
                    if (index >= 0)
                    {
                        editorsModel.set(i,{'filename':filename})
                        return
                    }
                }
            }
    }
}

function getModelIndexForFilepath(filepath) {
    var len=editorsModel.count;
    for (var i=0; i<len;i++)
        if (editorsModel.get(i)!=undefined)
            if (editorsModel.get(i).filepath == filepath)
                return i
    return -1;
}

function closeEditor(filepath) {
    console.log('closeEditor called')
    var len=editorsArray.length;
    for(var i=0; i<len; i++) {
            if (editorsArray[i].hasOwnProperty("filepath"))
            {
                if (editorsArray[i].filepath === filepath)
                {
                    var index = getModelIndexForFilepath(filepath);
                    if (index != -1)
                        editorsModel.remove(index);
                            
                    editorsArray[i].destroy();
                    editorsArray.splice(i,1);
                    console.log(editorsArray.length)
                    if (editorsArray.length > 0)
                        editors.currentTab = editorsArray[editorsArray.length - 1];
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

