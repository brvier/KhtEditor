import Qt 4.7
import net.khertan.qmlcomponents 1.0

Rectangle {
    id:win
    color: "grey"
    width:800
    height:480
    
    Flickable {
        id:flicker
        width: parent.width; height: parent.height
        contentWidth: editor.width; contentHeight: editor.height     
        clip: true
        QmlTextEditor {
            id:editor
            anchors.fill: parent
            onWidthChanged:{
                flicker.contentWidth=editor.width
            }
            onHeightChanged:{
                flicker.contentWidth=editor.width
            }
        }
    }
}



