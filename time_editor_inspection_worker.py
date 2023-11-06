import csv
import os
import time

from PyQt5 import QtCore
# from PyQt5.QtCore import QObject

from qgis.core import QgsVectorLayer, QgsPolygon, Qgis, QgsExpression, QgsGeometryEngine, QgsFeatureRequest, QgsGeometry, QgsSpatialIndex
from qgis.PyQt.QtCore import QCoreApplication

from .time_editor_date_helper import TimeEditorDateHelper

# also import pyqtRemoveInputHook
from qgis.PyQt.QtCore import pyqtRemoveInputHook

class TimeEditorInspectionWorker(QtCore.QObject):
    """Worker to inspect a Layer for time and/or spatial consistency"""

    def __init__(self, layer, check_type_idx=0, filter_expression=None, intersection_threshold=1.0):
        QtCore.QObject.__init__(self)
        if isinstance(layer, QgsVectorLayer) is False:
            raise TypeError(
                'Only Vector Layers can be inspected, got {}'.format(type(layer)))
        self.layer = layer
        self.filter_expression = filter_expression
        self.layer_idx = QgsSpatialIndex(
            self.layer.getFeatures(), 
            flags=QgsSpatialIndex.FlagStoreFeatureGeometries)
        self.killed = False
        self.date_helper = TimeEditorDateHelper()
        self.check_type_idx = check_type_idx

        self.INTERSECTION_THRESHOLD = intersection_threshold
    # Taken from plugin builder generated main file
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
        return QCoreApplication.translate('TimeEditor', message)

    def run(self):
        # TODO: better error handling (too large try ... except block)
        # try:
        all_date_series_valid = True
        life_start_name = self.layer.customProperty("te_time_start")
        life_start_idx = self.layer.dataProvider().fieldNameIndex(life_start_name)
        life_end_name = self.layer.customProperty("te_time_end")
        life_end_idx = self.layer.dataProvider().fieldNameIndex(life_end_name)
        common_id_name = self.layer.customProperty("te_common_id")
        common_id_idx = self.layer.dataProvider().fieldNameIndex(common_id_name)
        
        # TODO: old code, could use simple length from _get_all_features
        if self.layer.selectedFeatureCount() > 0:
            feature_count = self.layer.selectedFeatureCount()
        else:
            feature_count = self.layer.featureCount()

        all_features = self._get_all_features()

        # CASE 1: Handle Time Integrity Date Checking
        if self.check_type_idx == 0:
            # Load the csv file 
            time_integrity_exception_path = self.layer.customProperty("te_exception_csv_file")
            # id_exceptions is a simple list of concatenated strings 
            # of fids that are allowed to have a time gap, e.g. '313-314',
            # '320-391'
            # Any found Time Integrity issue will be checked against that list
            time_integrity_id_exceptions = []
            if os.path.exists(time_integrity_exception_path):
                with open(time_integrity_exception_path) as fh:
                    reader = csv.DictReader(fh)
                    for row in reader:
                        curr_ids = [int(row['fid1']), int(row['fid2'])]
                        curr_ids.sort()
                        id_exception = str(curr_ids[0]) + '-' + str(curr_ids[1])
                        time_integrity_id_exceptions.append(id_exception)
            # ensures that script only runs once per common id
            checked_common_ids = []
            idx = 0
            # Step is the number of features
            step = feature_count // 100
            if step == 0:
                step = 5
            for feature in all_features:
                if self.killed:
                    break
                idx += 1
                if idx % step == 0:
                    self.progress.emit(int(idx / float(feature_count) * 100))

                curr_common_id = feature.attribute(
                    feature.fieldNameIndex(common_id_name))
                if curr_common_id not in checked_common_ids:
                    checked_common_ids.append(curr_common_id)
                    # use current selection plus possibly existing expression 
                    sub_feature_expression = "{common_id_name} = '{common_id_value}'".format(
                        common_id_name=common_id_name,
                        common_id_value=curr_common_id
                    )
                    # take a possibly existing user filter into account
                    if (self.filter_expression):
                        sub_feature_expression = self.filter_expression + " and " + sub_feature_expression
                    all_sub_features = self.layer.getFeatures(sub_feature_expression)
                    # Collect all date vals to check for inconsistencies
                    curr_date_vals = []
                    for sub_feature in all_sub_features:
                        current_life_start = sub_feature.attribute(
                            sub_feature.fieldNameIndex(life_start_name))
                        current_life_end = sub_feature.attribute(
                            sub_feature.fieldNameIndex(life_end_name))
                        # Check if the date is valid for comparison / else abort
                        if not self.date_helper.validate_date_string(current_life_start)[0] \
                            or \
                        not self.date_helper.validate_date_string(current_life_end)[0]:
                            self.message.emit(
                                self.tr("Error: You have invalid dates. Please fix those dates using 'Date Integrity' before running this script."))
                            self.message.emit(
                                self.date_helper.validate_date_string(
                                    current_life_start)[0]
                            )
                            self.message.emit(
                                self.date_helper.validate_date_string(
                                    current_life_end)[0]
                            )
                            return
                        # TODO: Write utility function to safely retrieve attributes
                        if not isinstance(current_life_start, str):
                            if current_life_start.isNull():
                                current_life_start = ''
                        if not isinstance(current_life_end, str):
                            if current_life_end.isNull():
                                current_life_end = ''

                        curr_date_vals.append([
                            current_life_start,
                            current_life_end,
                            sub_feature.id(),
                            sub_feature.attribute(
                                sub_feature.fieldNameIndex(common_id_name))
                        ])
                    # Only check if more than one feature
                    # TODO: Should we make sanity checks for single timespan features?
                    if len(curr_date_vals) > 1:
                        curr_date_vals.sort()
                        # TODO: check: if all middle values have start and end set, see e.g.:
                        # [['', '1928-09-30', 79325, '631013130'], ['1928-10-01', '', 215, '631013130'], ['1928-10-01', '1971-12-31', 79324, '631013130'], ['1972-01-01', '', 79320, '631013130']]
                        # iterate over all collected dates to check validity
                        prev_date_val = [None, None]
                        for date_idx, date_val in enumerate(curr_date_vals):
                            if date_idx:
                                # print(date)
                                if not self.date_helper.dates_touch(prev_date_val[1], date_val[0]):
                                    # build an exception id string and check if 
                                    # it is in the csv-exceptions
                                    curr_ids = [prev_date_val[2], date_val[2]]
                                    curr_ids.sort()
                                    curr_id_exception = f"{curr_ids[0]}-{curr_ids[1]}"
                                    if curr_id_exception not in time_integrity_id_exceptions:
                                        self.validationIssue.emit([
                                            prev_date_val[2],
                                            date_val[2],
                                            date_val[3],
                                            # TODO: Add more information for csv export
                                            self.tr(f"End date '{prev_date_val[1]}' of {prev_date_val[2]} and start date '{date_val[0]}' of {date_val[2]} are not adjacent")
                                        ])
                                        all_date_series_valid = False

                            prev_date_val = date_val
            if not self.killed:
                if all_date_series_valid:
                    self.message.emit(
                        self.tr("Date history is valid for all features"))
                self.progress.emit(100)

        # CASE 2: Handle single feature date check
        elif self.check_type_idx == 1:
            all_dates_are_valid = True
            idx = 0
            step = 5
            for feature in all_features:
                if self.killed:
                    break
                idx += 1
                if idx % step == 0:
                    self.progress.emit(int(idx / float(feature_count) * 100))

                has_valid_start_date, start_date_error = self.date_helper.validate_date_string(
                    feature.attribute(life_start_idx))
                has_valid_end_date, end_date_error = self.date_helper.validate_date_string(
                    feature.attribute(life_end_idx))
                if not has_valid_start_date:
                    all_dates_are_valid = False
                    self.validationIssue.emit([
                        feature.id(),
                        self.tr("Invalid Start Date"),
                        start_date_error,
                    ])
                if not has_valid_end_date:
                    all_dates_are_valid = False
                    self.validationIssue.emit([
                        feature.id(),
                        self.tr("Invalid End Date"),
                        end_date_error
                    ])
            if not self.killed:
                self.progress.emit(100)
                if all_dates_are_valid:
                    self.message.emit(self.tr("All dates are valid"))
        # CASE 3: Handle spatial integrity check
        elif self.check_type_idx == 2:
            all_dates = []
            # getFeatures() will return an iterator, the plugin exhausts it once 
            # and will build a regular array (see function _get_all_features())
            # initial_id_selection = [feature.id() for feature in all_features]
            # Apparently there is no option to reset the Iterator, .rewind() only works
            # before exhaustion:
            # https://qgis-developer.qgis.narkive.com/bkbR1r2N/how-can-i-reset-the-starting-point-of-a-qgsfeatureiterator
            initial_id_selection = self.layer.selectedFeatureIds()
            # Now get all features with a possibly existing expression
            all_features = self._get_all_features()

            initial_id_selection_str = ", ".join(
                [str(_id) for _id in initial_id_selection])
            for feature in all_features:
                if self.killed:
                    return
                curr_start_date = feature.attribute(life_start_idx)
                curr_end_date = feature.attribute(life_end_idx)
                if isinstance(curr_start_date, str):
                    curr_start_date = str(curr_start_date).replace("??", "99")
                    if curr_start_date not in all_dates:
                        all_dates.append(curr_start_date)
                if isinstance(curr_end_date, str):
                    curr_end_date = str(curr_end_date).replace("??", "99")
                    if curr_end_date not in all_dates:
                        all_dates.append(curr_end_date)
            all_dates.sort()
            if len(all_dates) == 0:
                self.message.emit(
                    "All dates are set to NULL, use 1970-01-01 as a proxy to check spatial validity\n")
                all_dates = ["1970-01-01"]
            else:
                # the first date needs to be expanded, so the first state of the
                # feature selection will be checked too
                tmp_dates = [self.date_helper.get_adjacent_date(
                    all_dates[0], False)]
                tmp_dates.extend(all_dates)
                all_dates = tmp_dates

            for date_idx, date in enumerate(all_dates):
                self.progressFeature.emit(0)
                if self.killed:
                    return

                self.message.emit(self.tr("Checking timestamp ") + date)
                self.progress.emit(round(date_idx / len(all_dates) * 100))
                filter_str = self.date_helper.build_filter_string(
                    self.layer, date)
                filter_str += f"""\n AND "fid" in ({initial_id_selection_str})"""
                self.layer.setSubsetString(filter_str)
                self.refreshMap.emit()
                
                # get all currently selected features due to the layer filter
                curr_selected_feature_ids = [feature.id() for feature in self._get_all_features()]
                # in some cases the processing of the layer substring is apparently not 
                # ready and all initial (selected) features will be returned leading 
                # to a lot of intersections
                # Ideally we would have a signal to listen to, that the filter has been fully applied
                # For now we compare the numbers and repeat the loop until the subset has been applied
                tries = 0
                while len(curr_selected_feature_ids) == len(all_features):
                    time.sleep(1)
                    curr_selected_feature_ids = [feature.id() for feature in self._get_all_features()]
                    tries += 1
                    if tries > 5:
                        break
                if tries > 5:
                    self.message.emit("\nError in filtering features (same count for initial features and date-filtered features)\n")
                    continue 
                self.message.emit(f" ({len(curr_selected_feature_ids)} Features)\n")
                # for now it is unfortunately not possible using the topology checker
                # from pyqgs
                # https://gis.stackexchange.com/questions/280296/accessing-python-module-for-qgis-3-0-topology-checker-from-python-script
                # For now loop over all features and check for self-intersections
                # Add additional dialog to step through all years and perform topology check
                # manually
                # store features that have already been checked to avoid duplication
                checked_ids = []
                feature_step = 5
                # TODO: Use GeometryEngine
                # https://api.qgis.org/api/classQgsGeometryEngine.html
                # https://gitlab.uni-marburg.de/partner/hlgl/historische-karten/time-editor/-/issues/10
                for feature_idx, feature_id in enumerate(curr_selected_feature_ids):
                    if self.killed:
                        return
                    if feature_idx % feature_step == 0:
                        self.progressFeature.emit(
                            round((feature_idx / len(curr_selected_feature_ids)) * 100))
                    feature_geometry = self.layer_idx.geometry(feature_id)
                    feature_geometryengine = QgsGeometry.createGeometryEngine(
                        feature_geometry.constGet())
                    feature_geometryengine.prepareGeometry()
                    # Only check features intersecting the bounding box
                    overlapping_features = self.layer_idx.intersects(
                        feature_geometry.boundingBox())
                    for sub_feature_id in curr_selected_feature_ids:
                        if feature_id == sub_feature_id \
                            or \
                        sub_feature_id in checked_ids \
                            or \
                        sub_feature_id not in overlapping_features:
                            continue
                        sub_feature_geometry = self.layer_idx.geometry(
                            sub_feature_id)
                        # Leave as an example for debugging
                        # if feature_id == 1425 and sub_feature_id == 77917:
                        #     print("THIS SHOULD INTERSECT, BREAKING")
                        #     pyqtRemoveInputHook()
                        #     pdb.set_trace()
                        if feature_geometryengine.intersects(sub_feature_geometry.constGet()) or feature_geometryengine.overlaps(sub_feature_geometry.constGet()):
                            # https://api.qgis.org/api/classQgsGeometry.html#ab23decae1b7f7c962d0de1d47bff903a
                            curr_intersection = feature_geometryengine.intersection(
                                sub_feature_geometry.constGet())
                            if curr_intersection is not None:
                                # TODO: Transform GeometrySelections
                                curr_area = curr_intersection.area()
                                if curr_area > self.INTERSECTION_THRESHOLD:
                                    intersection_wkt = curr_intersection.asWkt()
                                    geom_type = curr_intersection.geometryType()
                                    sub_polys = []
                                    # collect only polygons from geometry collections
                                    # Simply concatenate the WKT representation
                                    if (geom_type == 'GeometryCollection'):
                                        for sub_geom in curr_intersection:
                                            if (sub_geom.geometryType() == 'Polygon'):
                                                sub_polys.append(
                                                    sub_geom.asWkt().replace("Polygon", "").strip())
                                        intersection_wkt = "MULTIPOLYGON(" + ",".join(
                                            sub_polys) + ")"

                                    self.validationIssue.emit([
                                        feature_id,
                                        sub_feature_id,
                                        date,
                                        # TODO: distinct between overlap and intersect
                                        "overlap",
                                        curr_area,
                                        intersection_wkt
                                    ])
                                    # self.message.emit(
                                    #     f"Feature {feature_id} and feature {sub_feature_id} overlap by {curr_area} (map units)\n")
                        checked_ids.append(feature_id)

                self.progressFeature.emit(100)
            self.message.emit("All dates have been checked\n")
            self.layer.setSubsetString("")
            self.refreshMap.emit()
            self.selectIds.emit(initial_id_selection)
            if not self.killed:
                self.progress.emit(100)

        # Case 4: Simple geometry valididty check (using isGeosValid())
        elif self.check_type_idx == 3:
            idx = 0
            step = 5
            all_valid = True

            for feature in all_features:
                if self.killed:
                    break
                idx += 1
                if idx % step == 0:
                    self.progress.emit(int(idx / float(feature_count) * 100))
                if not feature.geometry().isGeosValid():
                    errors = feature.geometry().validateGeometry()
                    errors = [error.what() for error in errors]
                    self.validationIssue.emit([
                        feature.id(),
                        "\n".join(errors)
                    ])
                    # self.message.emit(f"Feature {feature.id()} is not valid\n")
                    all_valid = False
            if not self.killed:
                if all_valid:
                    self.message.emit("All Features are geometrically valid.")

                self.progress.emit(100)

        # except Exception as e:
        #     # forward the exception upstream
        #     self.error.emit(e, traceback.format_exc())
        self.finished.emit()

    def kill(self):
        self.killed = True

    """
    Get all features, depending on active selection or empty selection -> all features
    Limit by the expression (if present). 
    If ignore_expression is set the present expression will be ignored (used internally 
    by restoring of the active Selection)
    """
    def _get_all_features(self, ignore_expression=False):
        if self.filter_expression is not None and ignore_expression == False:
            # Unfortunately selectedFeatures can not be filtered with 
            # a feature request 
            # https://qgis.org/pyqgis/master/core/QgsVectorLayer.html#qgis.core.QgsVectorLayer.getSelectedFeatures
            # request (QgsFeatureRequest = QgsFeatureRequest()) – You may specify 
            # a request, e.g. to limit the set of requested attributes. Any 
            # filter on the request will be discarded.
            # all_features = self.layer.getSelectedFeatures(featureRequest)
            
            # Solution for now: perform the subquery and filter by 
            # selectedFeatureIds
            
            # See above featureRequest not available on selectedFeatures 
            # -> always execute with .getFeatures
            # else:
            expression = QgsExpression(self.filter_expression)
            featureRequest = QgsFeatureRequest(expression)
            all_features = self.layer.getFeatures(featureRequest)
            all_features = [feature for feature in all_features]

            # only keep features that where selected
            if self.layer.selectedFeatureCount() > 0:
                all_selected_features_ids = self.layer.selectedFeatureIds()
                all_features = [feature for feature in all_features 
                        if feature.id() in all_selected_features_ids]
            # Dead code: 
                # Tried to extent the expression and pass the selected ids to the expression
                # all_feature_ids_as_str = ", ".join([str(_id) for _id in all_features_ids])
                # extended_expression = self.filter_expression + f' and array_contains(array({all_feature_ids_as_str}), "fid")'
                # print(extended_expression)
                # expression = QgsExpression(expression)
        else:
            if self.layer.selectedFeatureCount() > 0:
                all_features = self.layer.getSelectedFeatures()
            else:
                all_features = self.layer.getFeatures()
            # Create a regular python array for consistency (as active selection will have 
            # created one, too)
            all_features = [feature for feature in all_features]
        return all_features 
    
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(Exception, basestring)
    progress = QtCore.pyqtSignal(int)
    progressFeature = QtCore.pyqtSignal(int)
    validationIssue = QtCore.pyqtSignal(list)
    selectIds = QtCore.pyqtSignal(list)
    refreshMap = QtCore.pyqtSignal()
    message = QtCore.pyqtSignal(str)
