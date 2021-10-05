# -*- coding: utf-8 -*-
import os
from pathlib import Path
import sys

from qtpy.QtCore import (
    Qt,
)

from qtpy.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QHeaderView,
    QTableView,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from models import (
    AttributesTableModel,
    DataTableModel,
    DatasetTableModel,
    DimsTableModel,
    TreeModel,
)

from Pho_Import_Matlab_Data import import_mat_file


class HDF5Widget(QWidget):
    """
    Main HDF5 view container widget
    """

    def __init__(self, hdf):
        super().__init__()

        self.hdf = hdf

        # Initialise the models
        self.tree_model = TreeModel(self.hdf)
        self.attrs_model = AttributesTableModel(self.hdf)
        self.dataset_model = DatasetTableModel(self.hdf)
        self.dims_model = DimsTableModel(self.hdf)
        self.data_model = DataTableModel(self.hdf)

        # Set up the main file tree view
        self.tree_view = QTreeView(headerHidden=False)
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tree_view.setModel(self.tree_model)

        self.tree_view.header().setSectionResizeMode(0, QHeaderView.Interactive)
        self.tree_view.header().resizeSection(0, 160)
        self.tree_view.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tree_view.header().setStretchLastSection(True)

        # Setup attributes table view
        self.attrs_view = QTableView()
        self.attrs_view.setModel(self.attrs_model)
        self.attrs_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attrs_view.horizontalHeader().setStretchLastSection(True)
        self.attrs_view.verticalHeader().hide()

        # Setup dataset table view
        self.dataset_view = QTableView()
        self.dataset_view.setModel(self.dataset_model)
        self.dataset_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dataset_view.horizontalHeader().setStretchLastSection(True)
        self.dataset_view.verticalHeader().hide()

        # Setup attributes table view
        self.dims_view = QTableView()

        self.dims_view.setModel(self.dims_model)
        self.dims_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dims_view.horizontalHeader().setStretchLastSection(True)
        self.dims_view.verticalHeader().hide()

        # Setup main data table view
        self.data_view = QTableView()
        self.data_view.setModel(self.data_model)

        # Create the main layout. All the other
        # associated table views are placed in
        # surrounding dock widgets.
        layout = QVBoxLayout()
        layout.addWidget(self.data_view)
        self.setLayout(layout)

        # Finally, initialise the signals for the view
        self.init_signals()

    def init_signals(self):
        """
        Initialise the view signals
        """
        # Update the table views when a tree node is selected
        self.tree_view.selectionModel().selectionChanged.connect(self.handle_selection_changed)

        # Dynamically populate more of the tree items when
        # selected to keep memory usage at a minimum.
        self.tree_view.expanded.connect(self.tree_model.handle_expanded)
        self.tree_view.collapsed.connect(self.tree_model.handle_collapsed)

        self.dims_model.dataChanged.connect(self.handle_dims_data_changed)

    def close_file(self):
        """
        Close the hdf5 file and clean up
        """
        self.hdf.close()

    #
    # Slots
    #

    def handle_dims_data_changed(self, topLeft, bottomRight, roles):
        """
        Set the dimensions to display in the table
        """
        self.data_model.set_dims(self.dims_model.shape)

    def handle_selection_changed(self, selected, deselected):
        """
        When selection changes on the tree view
        update the node path on the models and
        refresh the data in the associated table
        views.
        """
        index = selected.indexes()[0]

        path = self.tree_model.itemFromIndex(index).data(Qt.UserRole)

        self.attrs_model.update_node(path)
        self.attrs_view.scrollToTop()

        self.dataset_model.update_node(path)
        self.dataset_view.scrollToTop()

        self.dims_model.update_node(path)
        self.dims_view.scrollToTop()

        self.data_model.update_node(path)
        self.data_view.scrollToTop()





if __name__ == "__main__":
    main_data_path = Path(r'/Volumes/iNeo/Data/Rotation_3_Kamran Diba Lab/ClusterFreeAnalysisProject/Data/Achilles_10252013')
    # spikesFilename = 'Achilles_10252013.spikes.cellinfo.mat'
    spikesFilename = main_data_path.joinpath('ExportedData', 'Achilles_10252013_spikes.mat')
    positionFilename = main_data_path.joinpath('ExportedData', 'Achilles_10252013_position.mat')
    # Computed
    spikesFileFullpath = main_data_path.joinpath(spikesFilename) # build a full filepath from the basepath
    positionFileFullpath = main_data_path.joinpath(positionFilename) # build a full filepath from the basepath

    temp_file = import_mat_file(positionFileFullpath)
    # data = build_tree_entries(temp_file)

    app = QApplication([])
    widget = HDF5Widget(temp_file)
    widget.show()
    # sys.exit(app.exec_())
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing window...')

