/****************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the QtDeclarative module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** No Commercial Usage
** This file contains pre-release code and may not be distributed.
** You may use this file in accordance with the terms and conditions
** contained in the Technology Preview License Agreement accompanying
** this package.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 2.1 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU Lesser General Public License version 2.1 requirements
** will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
** In addition, as a special exception, Nokia gives you certain additional
** rights.  These rights are described in the Nokia Qt LGPL Exception
** version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
**
** If you have questions regarding the use of this file, please contact
** Nokia at qt-info@nokia.com.
**
**
**
**
**
**
**
**
** $QT_END_LICENSE$
**
****************************************************************************/

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
        onClicked: toolbar.button2Clicked()
    }
    Button {
        id: button4
        anchors.left: button3.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button2Clicked()
    }
    Button {
        id: button5
        anchors.left: button4.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button2Clicked()
    }
    Button {
        id: button6
        anchors.left: button5.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button2Clicked()
    }
    Button {
        id: button7
        anchors.left: button6.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button2Clicked()
    }

    Button {
        id: button8
        anchors.left: button7.right;
        anchors.leftMargin: 8;
        anchors.top: parent.top;
        anchors.topMargin: 2;
        width: 90; height: 60
        onClicked: toolbar.button2Clicked()
    }


}
