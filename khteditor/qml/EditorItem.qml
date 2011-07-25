import QtQuick 1.1
import com.nokia.meego 1.0
import net.khertan.qmlcomponents 1.0

Page {
    property string filepath;
    property string filename;
//    proberty bool isNewFile;

//    id:editorPage
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
                text:((editor.modification) ? '* ':'')+ filepath;
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

        QmlTextEditor {
        //TextEdit{
           id:editor

            //width: 850
            //height:480

            onWidthChanged:{
                flicker.contentWidth=editor.width
            }
            onHeightChanged:{
                flicker.contentHeight=editor.height
            }
            onCursorRectangleChanged: {
                flicker.ensureVisible(cursorRectangle)
                }
            onPositionTextChanged: {
                toolTextPosition.text = positionText
                }
        }
    }

    function saveFile(){
        if (filepath.substr(0,1) == '/')
            editor.saveFile();
        else
            saveFileAs();

    }

    function setFilepath(filePath) {

        filepath = filePath
        filename = filePath.split('\\').pop().split('/').pop()
        editor.setFilepath(filePath)
        }

    function saveFileAs(){
        rootWin.pageStack.push(Qt.resolvedUrl('SaveAsPage.qml'))
    }

    function loadFile(filePath){
       filepath = filePath;
       filename = filePath.split('\\').pop().split('/').pop()
       editor.loadFile(filePath);
    }
    function comment(){
        editor.comment()
    }
    function indent(){
        editor.indent()
    }
    function unindent(){
        editor.unindent()
    }

}

