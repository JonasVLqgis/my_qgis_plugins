# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CopyCoordsToIfh
                                 A QGIS plugin
 Copy coordinates to an ifh importable format
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-04-14
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Jonas VL
        email                : jonasvl_qgis@outlook.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QComboBox

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .copy_coords_to_ifh_dialog import CopyCoordsToIfhDialog
import os.path

#3_Extra imports
import os
from PyQt5.QtCore import *
from qgis.core import *

#1_
from qgis.core import QgsProject

#1__
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtTest import QSignalSpy
from qgis.gui import QgsCheckableComboBox
from qgis.gui import *
from qgis.testing import start_app, unittest


class CopyCoordsToIfh:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CopyCoordsToIfh_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Copy Coords To Ifh')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CopyCoordsToIfh', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/copy_coords_to_ifh/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Copy Coords to IFH'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Copy Coords To Ifh'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = CopyCoordsToIfhDialog()
#2__
# Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()
#        print(layers)
# Clear the contents of the comboBox from previous runs
        self.dlg.mComboBox.clear()
# Populate the comboBox with names of all the loaded layers

        populate_box = []
        for layer in layers:
            if isinstance(layer, QgsLayerTreeGroup):
                layer_nodes = layer.findLayers()
                for lyr in layer_nodes:
                    populate_box.append(lyr.name())
            else:
                populate_box.append(layer.name())

#        self.dlg.mComboBox.addItems([layer.name() for layer in layers])
        self.dlg.mComboBox.addItems(populate_box)

		#Pre-checked layers
        checked_items_list = ['zones', 'phases']
        self.dlg.mComboBox.setCheckedItems(checked_items_list)
		

		
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed

        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
#            pass


            layer = None
            #requested_layers = ['dtps', 'ducts', 'zones', 'phases']
			#Fetch checkboxed layers
			# https://qgis.org/api/classQgsCheckableComboBox.html#a369062d3046261106ccaa41d6c922b9f
			#self.dlg.mComboBox.checkedItemsChanged
			#self.checkedItemsChanged.connect(self.dlg.mComboBox.checkedItems())
			#checkedItemsChanged
			#slot = setCheckedItems()
			#signal = checkedItemsChanged()
			

			
            requested_layers = self.dlg.mComboBox.checkedItems()
            print("Requested layers:", requested_layers)

			# Create directory coords
            dirName = 'coords'
            try:
				# Create target Directory
                os.mkdir(dirName)
                print("New folder " + dirName + " succesfully created") 
            except:
                print("Folder " + dirName + " already existed")

			#Pathing right
            absolute_project_path = (QFileInfo(QgsProject.instance().fileName())).absolutePath()
            print(absolute_project_path)

			#features ordenen volgens zone
            def get_zone_nr(f):
                return f['zone_nr']

			#converteren van coordinaten

            def convert_coords():
                if layer.wkbType() == QgsWkbTypes.Point:
                    for feature in my_features:
                        try:
                            identificator = str(feature['id'])
                        except:
                            identificator = "no id"
                        print(identificator)
                        output_file.write(identificator + '\n')
					#Geometrie van punt opvragen
                        pnt = feature.geometry().asPoint()
					#Formatting: 3 decimalen, toevoegen tab, punt vervangen door komma
                        obj_coords = ('%.3f' %pnt.x() + "\t" + '%.3f' %pnt.y()).replace(".", ",")
                        print(obj_coords)
                        output_file.write(obj_coords+ '\n')
                    output_file.close()
                    os.startfile(file_path)
							
                elif layer.wkbType() == QgsWkbTypes.MultiLineString:
                    for feature in my_features:
                        try:
                            identificator = str(feature['id'])
                        except:
                            identificator = "no id"
                        print(identificator)
                        output_file.write(identificator + '\n')
					#Geometrie van lijn opvragen
                        polyline = feature.geometry().asMultiPolyline()
						#print('Nummer: ', feature.attribute('zone_nr'))
					#Geometrie punt per punt van lijn opvragen
                        for pnt in polyline[0]:
					#Formatting: 3 decimalen, toevoegen tab, punt vervangen door komma
                            obj_coords = ('%.3f' %pnt.x() + "\t" + '%.3f' %pnt.y()).replace(".", ",")
                            print(obj_coords)
                            output_file.write(obj_coords+ '\n')
                    output_file.close()
                    os.startfile(file_path)
					
                elif layer.wkbType() == QgsWkbTypes.MultiPolygon:
                    for feature in my_features:
                        try:
                            identificator = str(feature['id'])
                        except:
                            identificator = "no id"
                        print(identificator)
                        output_file.write(identificator + '\n')
					#Geometrie van polygoon opvragen
                        polygon = feature.geometry().asMultiPolygon()
					#Geometrie punt per punt van polygoon opvragen
                        for pnt in polygon[0][0]:
					#Formatting: 3 decimalen, toevoegen tab, punt vervangen door komma
                            print(pnt.asWkt())
                            obj_coords = ('%.3f' %pnt.x() + "\t" + '%.3f' %pnt.y()).replace(".", ",")
                            print(obj_coords)
                            output_file.write(obj_coords+ '\n')
                    output_file.close()
                    os.startfile(file_path)
					
                else:
                    print("Error: conversion not available for this datatype")

            for lyr in QgsProject.instance().mapLayers().values():
                layer = lyr
                if layer.name() in requested_layers:
                    try:
                        my_features = sorted(layer.getFeatures(), key=get_zone_nr)
                    except:
                        my_features = layer.getFeatures()
                    file_path = absolute_project_path + "/coords/" + lyr.name() + ".txt"
                    output_file = open(file_path, "w")
                    print(QgsWkbTypes.displayString(int(layer.wkbType())), layer.name())
                    convert_coords()
                else:
                    pass

            if requested_layers != []:
                self.iface.messageBar().pushMessage("Success", "Export of coordinates completed in path:" + absolute_project_path + "/coords/", level=Qgis.Success, duration=5)
                print("\n Success: ", "Export of coordinates completed in path:" + absolute_project_path + "/coords/")
            else:
                self.iface.messageBar().pushMessage("Error", "No layers were requested", level=Qgis.Critical)
                print("\n Error: ", "No layers were requested")




