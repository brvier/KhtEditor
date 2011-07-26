import QtQuick 1.1
import com.nokia.meego 1.0
//import net.khertan.qmlcomponents 1.0
import 'editorCreation.js' as EditorCreation

Page {
    id: mainPage
    tools: editTools
    anchors.fill:parent

    Keys.onPressed:
        {
            if ( event.key == Qt.Key_S) editors.currentTab.saveFile()
            if ( event.key == Qt.Key_D) editors.currentTab.duplicate()
        }

    TabGroup {
            id:editors
            anchors.fill: parent
    }

    //Label {
    //    id:welcome
    //    anchors.fill: parent
    //    opacity: editors.currentTab === undefined ? 1.0 : 0.0
    //    text:'KhtEditor 3.0.0'
    //}

    ToolBarLayout {
        id: editTools
        visible: true
        //Line Number
        ToolButton {
            //text: editor.positionText
            id:toolTextPosition
            text: '000-000'
            flat: true
            width:120;
            onClicked: {

                       }
        }


        //Comment
        ToolIcon { platformIconId: "toolbar-tag";
            onClicked: editors.currentTab.comment()
        }
        //Indent
        ToolIcon { platformIconId: "toolbar-next";
            onClicked: editors.currentTab.indent()
        }
        //Unindent
        ToolIcon { platformIconId: "toolbar-previous";
            onClicked: editors.currentTab.unindent()
        }
        //Search
        ToolIcon { platformIconId: "toolbar-search";
            onClicked: notYetAvailableBanner.show()
        }

        //Execute
        ToolIcon { platformIconId: "toolbar-settings";
            onClicked: notYetAvailableBanner.show()
        }

        //Plugins
        ToolIcon { platformIconId: "toolbar-tools";
            onClicked: notYetAvailableBanner.show()
        }

        //List Opened File
        ToolIcon { platformIconId: "toolbar-pages-all";
            onClicked: {
                pageStack.push(Qt.resolvedUrl('OpenedPage.qml'))
            }


        }

        //Close
        ToolIcon { platformIconId: "toolbar-close";
            onClicked: closeFile();
        }

        //Menu
        ToolIcon { platformIconId: "toolbar-view-menu";
             anchors.right: parent===undefined ? undefined : parent.right;
             onClicked: (myMenu.status == DialogStatus.Closed) ? myMenu.open() : myMenu.close();
        }
    }


    function newFile() {
        console.log('newFile called');
        EditorCreation.createEditorObject();
    }

    function openFile(filepath) {
        EditorCreation.openEditorObject(filepath);
        //editors.currentTab.filepath = filepath
        //editors.currentTab.editor.load()
    }

    function saveFile() {
        if (editors.currentTab != undefined)
        {
            console.log(editors.currentTab)
            editors.currentTab.saveFile();
        }

    }

    function setFilepath(filepath) {
        editors.currentTab.setFilepath(filepath)
    }

    function saveAsFile() {
        if (editors.currentTab != undefined) {
            editors.currentTab.saveFileAs();
        }
    }

    function closeFile() {
        unsavedDialog.open()        
    }

    function switchFile(filepath){
        EditorCreation.switchEditor(filepath)
    }

    //function modificationsChanged(filepath,filename){
    //    EditorCreation.modificationsChanged(filepath, filename)
    //}

    QueryDialog {
	    id:unsavedDialog
	      titleText:"Unsaved"
	      message:"File is unsaved are you sure you want to close it ?";
	      acceptButtonText: 'Save';
	      rejectButtonText: 'Close';
		onAccepted: { editors.currentTab.saveFile();EditorCreation.closeEditor(editors.currentTab.filepath)}
		onRejected: { EditorCreation.closeEditor(editors.currentTab.filepath)}
    }
}

