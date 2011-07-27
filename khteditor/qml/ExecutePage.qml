import QtQuick 1.1
import com.nokia.meego 1.0
import net.khertan.qmlcomponents 1.0

Page {
    property string command;

    anchors.fill:parent
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
                text:'Running : ' + command;
                verticalAlignment: "AlignVCenter"
            }
        }


    Flickable {
        id:flicker
        width: parent.width; height: parent.height - 48
        contentWidth: editor.width; contentHeight: editor.height
        clip: true
        anchors.top: titlebar.bottom
        boundsBehavior:Flickable.DragOverBounds

        function ensureVisible(r){
             if (contentX >= r.x)
                 contentX = r.x;
             else if (contentX+width <= r.x+r.width)
                 contentX = r.x+r.width-width;
             if (contentY >= r.y)
                 contentY = r.y;
             else if (contentY+height <= r.y+r.height)
                 contentY = r.y+r.height-height;
         }

        QmlExecutor {
        //TextEdit{
           id:editor
        }
    }
}

