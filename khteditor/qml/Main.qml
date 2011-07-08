import Qt 4.7
import net.khertan.qmlcomponents 1.0

Rectangle {
    id:view
    color: "grey"
    width:800
    height:480

    property string filepath
    property string filename

    Rectangle {
        id:titlebar
        width:parent.width
        height:48
        anchors.top: parent.top
        color:'black'
        Text {
            id:titlelabel
            anchors.fill: parent
            font { bold: true; family: "Helvetica"; pixelSize: 18 }
            color:'white'
            text:view.filename + '\n' + view.filepath
            horizontalAlignment: "AlignHCenter"
            verticalAlignment: "AlignVCenter"
        }        
    }

    Flickable {
        id:flicker
        width: parent.width; height: parent.height - 64
        contentWidth: editor.width; contentHeight: editor.height     
        clip: true
        QmlTextEditor {
            id:editor
            filepath: view.filepath
            anchors.fill: parent
            onWidthChanged:{
                flicker.contentWidth=editor.width
            }
            onHeightChanged:{
                flicker.contentHeight=editor.height
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
