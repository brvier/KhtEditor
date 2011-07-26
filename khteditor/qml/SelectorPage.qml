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
            text:'Open File'
            verticalAlignment: "AlignVCenter"
        }
    }

//    FolderListModel {
//         id: folderModel
//         showDotAndDotDot: true
//         showDirs: true
//     }

    ListView {
        id: view
        anchors.top: pathbox.bottom
        height: parent.height - pathbox.height
        width: parent.width
        model: VisualDataModel {
            model: dirModel
            delegate: Rectangle {
                width:parent.width
                height: 80
                anchors.leftMargin: 10

//                Image {
//                    id: iconFile
//                    anchors.verticalCenter: parent.verticalCenter
//                    width: 64; height: 64
//                    source: fileIcon
//                }

                Column {
                    spacing: 10
                    //anchors.left: iconFile.left
                    anchors.leftMargin:10
                    anchors.left: parent.left
                    anchors.right: moreIcon.left

                    anchors.verticalCenter: parent.verticalCenter
                    Label {text:'<b>'+fileName+'</b>'
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 24
                        anchors.left: parent.left
                        anchors.right: parent.right

                    }
                    Label {text:filePath
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 16
                        color: "#cc6633"
                        anchors.left: parent.left
                        anchors.right: parent.right
                    }
                }
                Image {
                    id:moreIcon
                    source: "image://theme/icon-m-common-drilldown-arrow" + (theme.inverted ? "-inverse" : "")
                    anchors.right: parent.right;
                    anchors.verticalCenter: parent.verticalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        console.log(view.model.model)
                        if (view.model.model.isDir(view.model.modelIndex(index))){
                            titlelabel.text = 'Open File : ' + filePath
                            //previousFolderTool.currentFilePath = filePath
                            view.model.rootIndex = view.model.modelIndex(index)
                        }
                        else {
                            rootWin.openFile(filePath)
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
                titlelabel.text = 'Open File : ' + view.model.model.filePath(view.model.rootIndex)
            }

        }
    }
}

