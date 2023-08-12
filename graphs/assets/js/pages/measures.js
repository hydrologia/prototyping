var Highcharts;
var optionSelected;
var dropdown = $('#option_selector');
var url = 'https://raw.githubusercontent.com/hydrologia/prototyping/develop/warehouse/hydrometry/graphing/river/thames/menu/physicochemical.json';

// Menu Data
$.getJSON(url, function (data) {

    $.each(data, function (key, entry) {
        dropdown.append($('<option></option>').attr('value', entry.desc).text(entry.name));
    });

    // Load the first Option by default
    var defaultOption = dropdown.find("option:first-child").val();
    optionSelected = dropdown.find("option:first-child").text();

    // Generate
    generateChart(defaultOption);

});


// Dropdown
dropdown.on('change', function (e) {

    $('#option_selector_title').remove();

    // Save name and value of the selected option
    optionSelected = this.options[e.target.selectedIndex].text;
    var valueSelected = this.options[e.target.selectedIndex].value;

    //Draw the Chart
    generateChart(valueSelected);
});


// Generate graphs
function generateChart(fileNameKey) {

    $.getJSON('https://raw.githubusercontent.com/hydrologia/prototyping/develop/warehouse/hydrometry/graphing/river/thames/data/physicochemical/' + fileNameKey + '.json', function (source) {

        // https://api.highcharts.com/highstock/plotOptions.series.dataLabels
        // https://api.highcharts.com/class-reference/Highcharts.Point#.name
        // https://api.highcharts.com/highstock/tooltip.pointFormat


        // split the data set parts
        var temperature = [],
            ammonia = [],
            nitrate = [],
            potential = [],
            oxygen = [],
            turbidity = [],
            conductivity =[],
            dataLength = source.data.length,
            groupingUnits = [[
                'day',   // unit name
                [1]      // allowed multiples
            ]],
            i = 0;

        let columns = source.columns;
        var te = columns.indexOf('temp-i-subdaily-C'),
            am = columns.indexOf('amm-i-subdaily-mgL'),
            ni = columns.indexOf('nitrate-i-subdaily-mgL'),
            ph = columns.indexOf('ph-i-subdaily'),
            ox = columns.indexOf('do-i-subdaily-mgL'),
            tu = columns.indexOf('turb-i-subdaily-ntu'),
            co = columns.indexOf('cond-i-subdaily-uS');

        for (i; i < dataLength; i += 1) {

            temperature.push([
                source.data[i][0], // the date
                source.data[i][te] // temperature, Celsius
            ]);

            ammonia.push({
                x: source.data[i][0], // the date
                y: source.data[i][am] // ammonia, mg/L
            });

            nitrate.push({
                x: source.data[i][0], // the date
                y: source.data[i][ni] // nitrate, mg/L
            });

            potential.push({
                x: source.data[i][0], // date
                y: source.data[i][ph]  // potential of hydrogen
            });

            oxygen.push({
                x: source.data[i][0], // date
                y: source.data[i][ox]  // dissolved oxygen mg/L
            });

            turbidity.push({
               x: source.data[i][0], // date
               y: source.data[i][tu]  // turbidity NTU (nephelometric turbidity units)
            });

            conductivity.push({
               x: source.data[i][0], // date
               y: source.data[i][co]  // conductivity (microsiemens/centimetre)
            });

        }

        Highcharts.setOptions({
            lang: {
                thousandsSep: ','
            }
        });

        // Draw a graph
        Highcharts.stockChart('container0001', {

            rangeSelector: {
                selected: 1,
                verticalAlign: 'top',
                floating: false,
                inputPosition: {
                    x: 0,
                    y: 0
                },
                buttonPosition: {
                    x: 0,
                    y: 0
                },
                inputEnabled: true,
                inputDateFormat: '%Y-%m-%d'
            },

            chart: {
                zoomType: 'x'
                // borderWidth: 2,
                // marginRight: 100
            },

            title: {
                text: 'Curves of: ' + optionSelected
            },

            subtitle: {
                text: '<p>Hydrological Measures, The Waters of England</p> <br/> ' +
                    '<p><b>Data Source</b>: Environment Agency</p>'
            },

            time: {
                // timezone: 'Europe/London'
            },

            credits: {
                enabled: false
            },

            legend: {
                enabled: true,
                width: 500,
                x: 65
                // align: 'middle',
                // layout: 'vertical',
                // verticalAlign: 'bottom',
                // y: 10,
                // x: 35
            },

            caption: {
                // verticalAlign: "top",
                // y: 35,
                text: '<p>The graphs herein illustrate water quality measures vis-à-vis England\'s waters.  Each ' +
                    'measure has its own unit of measure, or does not have one.<br/><br/>NTU: Nephelometric Turbidity ' +
                    'Units, RFU: Relative Fluorescence Units, &mu;S/cm: microsiemens per centimetre, mg/L: milligrams per litre, &deg;C: Celsius</p>'
            },

            exporting: {
                buttons: {
                    contextButton: {
                        menuItems: [ 'viewFullscreen', 'printChart', 'separator',
                            'downloadPNG', 'downloadJPEG', 'downloadPDF', 'downloadSVG' , 'separator',
                            'downloadXLS', 'downloadCSV']
                    }
                }
            },

            yAxis: [{
                labels: {
                    align: 'left',
                    x: 5
                },
                title: {
                    text: 'Temp.',
                    align: 'middle',
                    x: 7
                },
                min: 0,
                height: '13%',
                lineWidth: 2,
                resize: {
                    enabled: true
                }
            }, {
                labels: {
                    align: 'left',
                    x: 5
                },
                title: {
                    text: 'Amm.',
                    align: 'middle',
                    x: 7
                },
                top: '14%',
                height: '13%',
                offset: 0,
                lineWidth: 2
            }, {
                title: {
                    text: 'Nitrate',
                    align: 'middle',
                    x: 7
                },
                top: '28%',
                height: '13%',
                offset: 0,
                lineWidth: 2
                }, {
                 labels: {
                     align: 'left',
                     x: 5
                 },
                 title: {
                     text: 'pH',
                     align: 'middle',
                     x: 7
                 },
                 top: '42%',
                 height: '13%',
                 offset: 0,
                 lineWidth: 2
               }, {
                 labels: {
                     align: 'left',
                     x: 5
                 },
                 title: {
                     text: 'DO',
                     align: 'middle',
                     x: 7
                 },
                 top: '56%',
                 height: '13%',
                 offset: 0,
                 lineWidth: 2
               }, {
                 labels: {
                     align: 'left',
                     x: 5
                 },
                 title: {
                     text: 'Turbidity',
                     align: 'middle',
                     x: 7
                 },
                 top: '70%',
                 height: '13%',
                 offset: 0,
                 lineWidth: 2
               }, {
                 labels: {
                     align: 'left',
                     x: 5
                 },
                 title: {
                     text: 'Cond.',
                     align: 'middle',
                     x: 7
                 },
                 top: '84%',
                 height: '13%',
                 offset: 0,
                 lineWidth: 2
               }
            ],

            plotOptions: {
                series: {
                    turboThreshold: 65000000
                }
            },

            tooltip: {
                split: true,
                dateTimeLabelFormats: {
                    millisecond: "%A, %e %b, %H:%M:%S.%L",
                    second: "%A, %e %b, %H:%M:%S",
                    minute: "%A, %e %b, %H:%M",
                    hour: "%A, %e %b, %H:%M",
                    day: "%A, %e %B, %Y",
                    week: "%A, %e %b, %Y",
                    month: "%B %Y",
                    year: "%Y"
                }

            },

            series: [{
                type: 'spline',
                name: 'Temperature',
                data: temperature,
                dataGrouping: {
                    units: groupingUnits,
                    dateTimeLabelFormats: {
                        millisecond: ['%A, %e %b, %H:%M:%S.%L', '%A, %b %e, %H:%M:%S.%L', '-%H:%M:%S.%L'],
                        second: ['%A, %e %b, %H:%M:%S', '%A, %b %e, %H:%M:%S', '-%H:%M:%S'],
                        minute: ['%A, %e %b, %H:%M', '%A, %b %e, %H:%M', '-%H:%M'],
                        hour: ['%A, %e %b, %H:%M', '%A, %b %e, %H:%M', '-%H:%M'],
                        day: ['%A, %e %b, %Y', '%A, %b %e', '-%A, %b %e, %Y'],
                        week: ['Week from %A, %e %b, %Y', '%A, %b %e', '-%A, %b %e, %Y'],
                        month: ['%B %Y', '%B', '-%B %Y'],
                        year: ['%Y', '%Y', '-%Y']
                    }
                },
                tooltip: {
                    pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {series.name}</b>: ' +
                        '{point.y:,.2f}&deg;C<br/>'
                }
            },
                {
                    type: 'spline',
                    name: 'Ammonia',
                    data: ammonia,
                    color: '#6B8E23',
                    yAxis: 1,
                    dataGrouping: {
                        units: groupingUnits
                    },
                    tooltip: {
                        pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {series.name}</b>: ' +
                            '{point.y:,.2f} mg/L<br/>'
                    }
                },
                {
                    type: 'spline',
                    name: 'Nitrate',
                    data: nitrate,
                    color: '#A08E23',
                    visible: true,
                    yAxis: 2,
                    dataGrouping: {
                        units: groupingUnits
                    },
                    tooltip: {
                        pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {series.name}</b>: ' +
                            '{point.y:,.2f} mg/L<br/>'
                    }
                },
                {
                    type: 'spline',
                    name: 'pH',
                    data: potential,
                    color: '#EDC948',
                    yAxis: 3,
                    dataGrouping: {
                        units: groupingUnits
                    },
                    tooltip: {
                        pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {series.name}</b>: ' +
                            '{point.y:,.2f}<br/>'
                    }
                },
                {
                    type: 'spline',
                    name: 'Dissolved Oxygen',
                    data: oxygen,
                    color: '#800000',
                    yAxis: 4,
                    dataGrouping: {
                        units: groupingUnits
                    },
                    tooltip: {
                        pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {series.name}</b>: ' +
                            '{point.y:,.2f} mg/L<br/>'
                    }

                },
                 {
                     type: 'spline',
                     name: 'Turbidity',
                     description: 'Nephelometric Turbidity Units',
                     data: turbidity,
                     color: '#000000',
                     yAxis: 5,
                     dataGrouping: {
                         units: groupingUnits
                     },
                     tooltip: {
                         pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {series.name}</b>:<br/>' +
                             '{point.y:,.2f} NTU<br/>'
                     }

                 },
                   {
                       type: 'spline',
                       name: 'Conductivity',
                       description: 'microsiemens per centimetre',
                       data: conductivity,
                       color: '#006600',
                       yAxis: 6,
                       dataGrouping: {
                           units: groupingUnits
                       },
                       tooltip: {
                           pointFormat: '<span style="color:{point.color}">\u25CF</span> <b> {series.name}</b>:<br/>' +
                               '{point.y:,.2f} &mu;S/cm<br/>'
                       }

                   }


            ],
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 700
                    },
                    chartOptions: {
                        rangeSelector: {
                            inputEnabled: false
                        }
                    }
                }]
            }
        });

    }).fail(function () {
        console.log("Missing");
        $('#container0001').empty();
    });

}

