import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id:openedEditors
    anchors.fill:parent
    tools: backTool

    Component {
        id:openedEditorsDelegate
        Item {
            width:parent.width
            height: 80
            anchors.leftMargin: 10

            Column {
                spacing: 10
                anchors.horizontalCenter: parent.horizontalCenter
                Label {text:'<b>'+filename+'</b>'
                    font.family: "Nokia Pure Text"
                    font.pixelSize: 24
                }
                Label {text:filepath
                    font.family: "Nokia Pure Text"
                    font.pixelSize: 16
                    color: "#cc6633"
                }
            }
            Image {
                //source: "image://theme/icon-m-common-drilldown-arrow" + (theme.inverted ? "-inverse" : "")
                anchors.right: parent.right;
                anchors.verticalCenter: parent.verticalCenter
            }

            MouseArea {
                id: mouseArea
                anchors.fill: parent
                onClicked: {
                    rootWin.switchFile(filepath)
                }
            }
        }
    }

    Rectangle {
        id:titlebar
        width:parent.width
        height:48
        anchors.top: parent.top
        color:'black'
        Text {
            id:titlelabel
            anchors.fill: parent
            anchors.leftMargin: 5
            font { bold: true; family: "Helvetica"; pixelSize: 18 }
            color:"#cc6633"
            text:'Currently Opened Files'
            verticalAlignment: "AlignVCenter"
        }
    }

    ListView {
        id:openedEditorsView
        anchors.top:titlebar.bottom
        anchors.topMargin: 10
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.bottomMargin: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        delegate:openedEditorsDelegate
        model:editorsModel
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
