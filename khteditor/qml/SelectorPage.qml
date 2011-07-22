import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id:openedEditors
    anchors.fill:parent
    tools: backTool

    Rectangle {
        id:pathbox
        width:parent.width
        height:40
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

                Column {
                    spacing: 10
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
                    source: "image://theme/icon-m-common-drilldown-arrow" + (theme.inverted ? "-inverse" : "")
                    anchors.right: parent.right;
                    anchors.verticalCenter: parent.verticalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (model.hasModelChildren){
                            titlelabel.text = 'Open File : ' + filePath
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
    }
}
