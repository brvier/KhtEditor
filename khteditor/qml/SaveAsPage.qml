import QtQuick 1.1
import com.nokia.meego 1.0
//import Qt.labs.folderlistmodel 1.0

Page {
    id:openedEditors
    anchors.fill:parent
    tools: backTool


    Rectangle {
        id:pathbox
        width:parent.width
        height:48
        color:'black'
        Text{
            id:titlelabel
            anchors.fill: parent
            anchors.leftMargin: 5
            font { bold: true; family: "Helvetica"; pixelSize: 18 }
            color:"#cc6633"
            text:'Save File As: /' + filename.text
            verticalAlignment: "AlignVCenter"
        }
    }

   Rectangle {
            id: filesavebox
            anchors.top: pathbox.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height:80
            color: 'white'
            Label {
                id:filenamelabel;
                text:'File name : ';
                width: 150
                font { bold: true; family: "Helvetica"; pixelSize: 24 }
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
            }

            TextField {
                id:filename
                anchors.left: filenamelabel.right
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter

                onTextChanged: {
                    titlelabel.text = 'Save File As : ' + view.model.model.filePath(view.model.rootIndex)  + '/' + filename.text
                }
            }
        }

   Rectangle {
        color:'white'
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: filesavebox.bottom

        Label {
                id:folderlabel;
                text:'Folder :';
                height: 80
                width: 150
                font { bold: true; family: "Helvetica"; pixelSize: 24 }
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
            }

        ListView {
            id: view
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.right:  parent.right
            anchors.left: folderlabel.right
            model: VisualDataModel {
                model: dirModel
                delegate: Rectangle {
                    width:parent.width
                    height: 80
                    anchors.leftMargin: 10

                    Column {
                        spacing: 10
                        //anchors.left: iconFile.left
                        anchors.leftMargin:10

                        anchors.verticalCenter: parent.verticalCenter
                        Label {text:'<b>'+fileName+'</b>'
                            font.family: "Nokia Pure Text"
                            font.pixelSize: 24
                        }
                        Label {text:filePath
                            font.family: "Nokia Pure Text"
                            font.pixelSize: 16
                            color: "#cc6633"
                        }
                    }
                    Image {
                        //source: view.model.model.isDir(view.model.modelIndex(index)) ? "image://theme/icon-m-common-drilldown-arrow" : ''
                        source: 'image://theme/icon-m-common-drilldown-arrow'
                        anchors.right: parent.right;
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            console.log(view.model.model)
                            if (view.model.model.isDir(view.model.modelIndex(index))){
                                titlelabel.text = 'Save File As : ' + filePath + '/' +  filename.text
                                //previousFolderTool.currentFilePath = filePath
                                view.model.rootIndex = view.model.modelIndex(index)
                            }
                            else {

                            }
                        }

                    }
                }
            }
        }
    }


    ToolBarLayout {
        id:backTool
        visible: true
        ToolIcon {
            platformIconId: 'toolbar-back'
            onClicked: pageStack.pop()
        }
        ToolIcon {
            id: previousFolderTool
            //property string currentIndex;
            platformIconId: 'toolbar-up'
            anchors.right: parent.right
            onClicked: {
                view.model.rootIndex = view.model.parentModelIndex()
                titlelabel.text = 'Save File As : ' + view.model.model.filePath(view.model.rootIndex)  + '/' + filename.text
            }
        }
        ToolButton {
            id: saveTool
            flat: true
            text:'Save'
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: {
                rootWin.saveFileAs(view.model.model.filePath(view.model.rootIndex) + '/' + filename.text)
                console.log(view.model.model.filePath(view.model.rootIndex) + '/' + filename.text)
            }
        }
    }
}

