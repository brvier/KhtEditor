import QtQuick 1.1
import com.nokia.meego 1.0
//import Qt.labs.folderlistmodel 1.0

Page {
    id:settingsPage
    anchors.fill:parent
    tools: settingsTool

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
                font { bold: true; family: "Nokia Pure Text"; pixelSize: 18 }
                color:"#cc6633"
                text:"Preferences";
                verticalAlignment: "AlignVCenter"
            }
            
            Image{
                id:closeButton
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.topMargin: 2
                opacity: closeButtonArea.pressed ? 0.5 : 1.0
                source:"image://theme/icon-m-common-dialog-close"
                MouseArea{
                    id:closeButtonArea
                    anchors.fill: parent
                    onClicked: pageStack.pop()
                }
            }
            
            //The real prefs gui start here
            Label {
                id:fontnamelabel
                anchors.top: titlebar.bottom
                anchors.left: parent.left
                anchors.leftMargin: 5
                anchors.topMargin: 10
                text:"Font Name";
            }

            //The real prefs gui start here
            Label {
                id:fontsizelabel
                anchors.top: fontnamelabel.bottom
                anchors.left: parent.left
                anchors.leftMargin: 5
                anchors.topMargin: 10
                text:"Font Size";
            }
    }

    ToolBarLayout {
        id:settingsTool
        visible: true
        ToolIcon {
            platformIconId: 'toolbar-back'
            onClicked: pageStack.pop()
        }
    }
}

