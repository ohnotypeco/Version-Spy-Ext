import platform
import textwrap

from AppKit import NSApp, NSMenuItem, NSPasteboard, NSPasteboardTypeString
from mojo.events import addObserver, removeObserver
from mojo.roboFont import version as RFversion
from mojo.roboFont import buildNumber as RFBuildNumber
from mojo.tools import CallbackWrapper
from mojo.UI import PostBannerNotification

class VersionSpy:
    def __init__(self):
        addObserver(self, "waitForActive", "applicationDidFinishLaunching")

    def waitForActive(self, info):
        addObserver(self, "addMenuItem", "applicationDidBecomeActive")

    def addMenuItem(self, info):
        removeObserver(self, "applicationDidBecomeActive")
        removeObserver(self, "applicationDidFinishLaunching")

        menubar = NSApp().mainMenu()

        # RoboFont > Copy Version Info...
        title = "Copy Version Info…"
        # Find the RoboFont menu
        roboMenu = menubar.itemAtIndex_(0)
        # Get the submenu
        roboSubMenu = roboMenu.submenu()
        # Check if the menu item already exists
        copyVersionInfoItem = roboSubMenu.itemWithTitle_(title)
        if not copyVersionInfoItem:
            # If it doesn't exist, create a new NSMenuItem with the title "Copy Version Info..." and add it to the menu below the About item
            self.copyVersionInfoTarget = CallbackWrapper(self.copyVersionInfoCallback)
            copyVersionInfoItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                title,
                "action:",
                ""
            )
            copyVersionInfoItem.setTarget_(self.copyVersionInfoTarget)
            roboSubMenu.insertItem_atIndex_(copyVersionInfoItem, 1)

        # Finally, rename "RoboFont" to include the version number
        roboMenu.submenu().setTitle_("RoboFont %s" % RFversion)

    def copyVersionInfoCallback(self, sender):
        versionInfo = f"""\
        RoboFont {RFversion} ({RFBuildNumber})
        Python {platform.python_version()}
        MacOS {platform.mac_ver()[0]} ({platform.uname().system} {platform.uname().release})
        Processor {platform.processor()} ({platform.machine()})
        """
        versionInfo = textwrap.dedent(versionInfo).strip()

        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.declareTypes_owner_([NSPasteboardTypeString], None)
        pasteboard.setString_forType_(versionInfo, NSPasteboardTypeString)

        PostBannerNotification("Copy Version Info", "Copied version info to the clipboard")


VersionSpy()
