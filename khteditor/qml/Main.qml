import QtQuick 1.0
import net.khertan.qmlcomponents 1.0

Item {
    id: window

    Flickable{
        id: flicker
        width: parent.width
        height: parent.height
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
    
    ScrollBar{
        id:texteditscroller
        scrollArea: flicker
        width: 10
        anchors.right: parent.right
        height: parent.height
    }

    MessageBox{
        id:message
        opacity: 0

    }

    ToolBar{
        id:toolbar
        height:64
        width: parent.width
        anchors.bottom: parent.bottom
        button1Icon: "Images/comment.png"
        button2Icon: "Images/indent.png"
        button3Icon: "Images/unindent.png"
        button4Icon: "Images/search.png"
        button5Icon: "Images/open.png"
        button6Icon: "Images/save.png"
        button7Icon: "Images/execute.png"
        button8Icon: "Images/execute.png"
        onButton1Clicked:
        {
            message.text='This feature is not yet implemented';
            message.opacity=1
        }
        onButton2Clicked:
        {
            message.text='This feature is not yet implemented';
            message.opacity=1
        }
    }

}
