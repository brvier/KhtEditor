import Qt 4.7

Item {
    id: toolbar

    property alias button1Label: button1.text
    property alias button2Label: button2.text
    property alias button3Label: button3.text
    property alias button4Label: button4.text
    property alias button5Label: button5.text
    property alias button6Label: button6.text
    property alias button7Label: button7.text
    property alias button8Label: button8.text
    property alias button1Icon: button1.icon
    property alias button2Icon: button2.icon
    property alias button3Icon: button3.icon
    property alias button4Icon: button4.icon
    property alias button5Icon: button5.icon
    property alias button6Icon: button6.icon
    property alias button7Icon: button7.icon
    property alias button8Icon: button8.icon
    signal button1Clicked
    signal button2Clicked
    signal button3Clicked
    signal button4Clicked
    signal button5Clicked
    signal button6Clicked
    signal button7Clicked
    signal button8Clicked
    focus:true
    
    BorderImage { source: "Images/titlebar.sci"; width: parent.width; height: parent.height + 14; y: -7 }
    Button {
        id: button1
        anchors.left: parent.left;
        anchors.leftMargin: 12;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button1Clicked()
        focus:true
    }
    Button {
        id: button2
        anchors.left: button1.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button2Clicked()
    }
    Button {
        id: button3
        anchors.left: button2.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button3Clicked()
    }
    Button {
        id: button4
        anchors.left: button3.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button4Clicked()
    }
    Button {
        id: button5
        anchors.left: button4.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button5Clicked()
    }
    Button {
        id: button6
        anchors.left: button5.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button6Clicked()
    }
    Button {
        id: button7
        anchors.left: button6.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button7Clicked()
    }

    Button {
        id: button8
        anchors.left: button7.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button8Clicked()
    }


}
