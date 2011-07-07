import Qt 4.7

Item {
    width: parent.width / 1.2
    height: 62
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.verticalCenter: parent.verticalCenter
    z: 5
    BorderImage { source: "Images/toolbutton.sci"; width: parent.width; height: parent.height + 14; y: -7 }

    property alias text: messageText.text

    Text {
        id: messageText
        anchors.fill: parent
        text:  ""

        width: parent.width / 4
        height: 50
        color: "#FFFFFF"
        font { bold: true; family: "Helvetica"; pixelSize: 18 }
        horizontalAlignment: "AlignHCenter"
        verticalAlignment: "AlignVCenter"
    }
    MouseArea {
        anchors.fill: parent
        onClicked: parent.opacity = 0
    }
    Behavior on opacity { NumberAnimation { duration: 100 } }
}
