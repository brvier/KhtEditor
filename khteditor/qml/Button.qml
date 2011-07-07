import Qt 4.7

Item {
    id: container

    signal clicked

    property string text
    property string icon
    property bool keyUsing: false

    BorderImage {
        id: buttonImage
        opacity: 0.5
        source: "Images/toolbutton.sci"
        width: container.width; height: container.height
    }
    BorderImage {
        id: pressed
        opacity: 0
        source: "Images/toolbutton.sci"
        width: container.width; height: container.height
    }
    MouseArea {
        id: mouseRegion
        anchors.fill: buttonImage
        onClicked: { container.clicked(); }
    }
    Text {
        id: btnText
        color: if(container.keyUsing){"#D0D0D0";} else {"#FFFFFF";}
        anchors.centerIn: buttonImage; font.bold: true
        text: container.text; style: Text.Raised; styleColor: "black"
        font.pixelSize: 12
    }
    Image{
        id: btnIcon
        fillMode: Image.PreserveAspectFit
        anchors.centerIn: buttonImage;
        source: container.icon
        width: container.width - 5; height: container.height - 5
    }

    states: [
        State {
            name: "Pressed"
            when: mouseRegion.pressed == true
            PropertyChanges { target: pressed; opacity: 1 }
        },
        State {
            name: "Focused"
            when: container.activeFocus == true
            PropertyChanges { target: btnText; color: "#FFFFFF" }
        }
    ]
    transitions: Transition {
        ColorAnimation { target: btnText; }
    }
}
