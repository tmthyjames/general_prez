(function() {

	// See: https://github.com/dc-js/dc.js/issues/878
	var compositeChart = dc.compositeChart;
    dc.compositeChart = function(parent, chartGroup) {
        var _chart = compositeChart(parent, chartGroup);
        
        _chart._brushing = function () {
            var extent = _chart.extendBrush();
            var rangedFilter = null;
            if(!_chart.brushIsEmpty(extent)) {
                rangedFilter = dc.filters.RangedFilter(extent[0], extent[1]);
            }

            dc.events.trigger(function () {
                if (!rangedFilter) {
                    _chart.filter(null);
                } else {
                    _chart.replaceFilter(rangedFilter);
                }
                _chart.redrawGroup();
            }, dc.constants.EVENT_DELAY);
        };
        
        return _chart;
    };

    var rowChart = dc.rowChart;
    dc.rowChart = function(parent, chartGroup) {
    	var _chart = rowChart(parent, chartGroup);

    	_chart.singleSelect = function(on) {
    		if (!on) return _chart;

    		_chart.on('pretransition', function(chart) {
				_chart.selectAll("g[class^=row]").on("click", function (d) {
					//console.log('click:', d.key)
					_chart.filter(null)
					.filter(d.key)
					.redrawGroup();
				});
			});

    		return _chart; 
    	}

    	return _chart;
    }
})();