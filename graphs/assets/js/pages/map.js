// In progress
(async () => {

    const topology = await fetch(
        'https://code.highcharts.com/mapdata/countries/gb/gb-all.topo.json'
    ).then(response => response.json());

    // Initialize the chart
    Highcharts.mapChart('container', {

        chart: {
            map: topology
        },

        title: {
            text: 'Latitude, Longitude'
        },

        accessibility: {
            description: 'Details Upcoming'
        },

        mapNavigation: {
            enabled: true
        },

        tooltip: {
            headerFormat: '',
            pointFormat: '<b>{point.name}</b><br>Latitude: {point.lat}, Longitude: {point.lon}'
        },

        series: [{
            // The gb-all map, without data, as the basemap
            name: 'Great Britain',
            borderColor: '#A0A0A0',
            nullColor: 'rgba(200, 200, 200, 0.3)',
            showInLegend: false
        }, {
            name: 'Separators',
            type: 'mapline',
            nullColor: '#707070',
            showInLegend: false,
            enableMouseTracking: false,
            accessibility: {
                enabled: false
            }
        }, {
            // Specify points using latitude/longitude
            type: 'mappoint',
            name: 'Stations',
            accessibility: {
                point: {
                    valueDescriptionFormat: '{xDescription}. Latitude: {point.lat:.2f}, Longitude: {point.lon:.2f}.'
                }
            },
            color: Highcharts.getOptions().colors[1],
            data: []
        }]
    });

})();