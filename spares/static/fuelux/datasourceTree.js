/*
 * Fuel UX Data components - static data source
 * https://github.com/ExactTarget/fuelux-data
 *
 * Copyright (c) 2012 ExactTarget
 * Licensed under the MIT license.
 */

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['underscore'], factory);
    } else {
        root.TreeDataSource = factory();
    }
}(this, function () {

    var DataSourceTree = function (options) {
        this._data = options.data;
        this._typ_id = options.typ_id;
        this._delay = options.delay;
    };

    DataSourceTree.prototype = {

        data: function (options, callback) {
            var self = this;

            setTimeout(function () {

                $.ajax("/spares-load/", {

                    dataType: 'json',
                    data: { typ_id: self._typ_id, str_id: options.additionalParameters ? options.additionalParameters.id.replace('node', '') : 0}

                }).done(function (response) {
                        var data = $.extend(true, [], response.data);

                        callback({ data: data });
                    });

            }, self._delay);
        }

    };

    return DataSourceTree;
}));
