import QtQuick 1.1
import com.nokia.meego 1.0
//import Qt.labs.folderlistmodel 1.0

Page {
    id:openedEditors
    anchors.fill:parent
    tools: aboutTool

    Rectangle {
        id:welcomeRect
        anchors.fill: parent
        
        Image {
            id:logo
            source: Qt.resolvedUrl('../icons/khteditor.png')
            anchors.top: parent.top
            anchors.topMargin: 20
            height: 80
            width: 80
            anchors.horizontalCenter: parent.horizontalCenter
            //horizontalAlignment: "AlignHCenter"        
        }

    Label {
            id: versionLabel
            text:'<b>KhtEditor</b><br>Version ' + __version__
            font.family: "Nokia Pure Text"
            font.pixelSize: 24
                        
            anchors.top: logo.bottom
            anchors.topMargin: 20
            anchors.left: parent.left
            anchors.right: parent.right
            horizontalAlignment: "AlignHCenter"
        }

    Label {
            id:authorLabel
            text:'By <b>Benoît HERVIER (Khertan)</b><br>http://khertan.net/'
            font.family: "Nokia Pure Text"
            font.pixelSize: 20
                        
            anchors.top: versionLabel.bottom
            anchors.topMargin: 20
            anchors.left: parent.left
            anchors.right: parent.right
            horizontalAlignment: "AlignHCenter"
        }

    Label {
            id:licenceLabel
            text:'A source code editor for MeeGo and Harmattan<br><b>Licenced under GPLv3</b>'
            font.family: "Nokia Pure Text"
            font.pixelSize: 20
                        
            anchors.top: authorLabel.bottom
            anchors.topMargin: 20
            anchors.left: parent.left
            anchors.right: parent.right
            horizontalAlignment: "AlignHCenter"
        }

    Button {
            id:launchWWW
            text: 'View Khertan.net website'
            anchors.bottom: parent.bottom
            anchors.bottomMargin:10
            anchors.left: parent.left
            anchors.leftMargin: 50
            height: 60
            onClicked:{Qt.openUrlExternally('http://khertan.net/')}
        }

    Button {
            id:launchWWWBT
            text: 'View KhtEditor BugTracker'
            anchors.bottom: parent.bottom
            anchors.bottomMargin:10
            anchors.right: parent.right
            anchors.rightMargin: 50
            height: 60            
            onClicked:{Qt.openUrlExternally('http://khertan.net/khteditor:bugs')}
        }

    }

    ToolBarLayout {
        id:aboutTool
        visible: true
        ToolIcon {
            platformIconId: 'toolbar-back'
            onClicked: pageStack.pop()
        }
    }
}

