import Qt 4.7
import com.nokia.meego 1.0

import net.khertan.qmlcomponents 1.0

PageStackWindow {
    id: appWindow

    initialPage: mainPage

    MainPage{
	id: mainPage
   	color: "grey"
	width: 800
	height: 480
    	Flickable {
        	id: flick
		
        	width: 800; height: 480;
        	contentWidth: children.width; contentHeight: children.height
        	clip: true
        	QmlTextEditor {
           		id:editor
           		width: parent.width; height: parent.height;
            		anchors.centerIn: parent
        		}
    		}
	}

    ToolBarLayout {
        id: commonTools
        visible: true
        ToolIcon { platformIconId: "toolbar-view-menu";
             anchors.right: parent===undefined ? undefined : parent.right
             onClicked: (myMenu.status == DialogStatus.Closed) ? myMenu.open() : myMenu.close()
        }
    }

    Menu {
        id: myMenu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: "Sample menu item" }
        }
    }
}
