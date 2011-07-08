import Qt 4.7

Item {
    id: toolbar

    property alias lineNumberButtonLabel: lineNumberButton.text
    signal commentButtonClicked
    signal indentButtonClicked
    signal unIndentButtonClicked
    signal button4Clicked
    signal button5Clicked
    signal button6Clicked
    signal button7Clicked
    signal button8Clicked
    focus:true
    
    BorderImage { source: "Images/titlebar.sci"; width: parent.width; height: parent.height + 14; y: -7 }
    Button {
        id: lineNumberButton
        text: '001-001'
        anchors.left: parent.left
        anchors.leftMargin: 12
        anchors.top: parent.top
        anchors.topMargin: 2
        width: 90; height: 60
        onClicked: toolbar.lineNumberButtonClicked()
        focus:true
    }
    Button {
        id: commentButton
        icon: 'Images/comment.png'
        anchors.left: lineNumberButton.right
        anchors.leftMargin: 8
        anchors.top: parent.top
        anchors.topMargin: 2
        width: 90; height: 60
        onClicked: toolbar.commentButtonClicked()
    }
    Button {
        id: indentButton
        icon: 'Images/indent.png'
        anchors.left: commentButton.right
        anchors.leftMargin: 8
        anchors.top: parent.top
        anchors.topMargin: 2
        width: 90; height: 60
        onClicked: toolbar.indentButtonClicked()
    }
    Button {
        id: unIndentButton
        icon: 'Images/unindent.png'
        anchors.left: indentButton.right;
        anchors.leftMargin: 8
        anchors.top: parent.top
        anchors.topMargin: 2
        width: 90; height: 60
        onClicked: toolbar.unIndentButtonClicked()
    }
    Button {
        id: button5
        anchors.left: unIndentButton.right;
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
