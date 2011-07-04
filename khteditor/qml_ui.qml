import Qt 4.7
import net.khertan.qmlcomponents 1.0

Rectangle {
    color: "grey"
    width:800
    height:480
    Flickable {
        id: flick
        width: parent.width - 10; height: parent.height;
        clip: true
        QmlTextEditor {
            id:editor
            width: parent.width; height: parent.height;                
            anchors.centerIn: parent            
        }
    }
}

