
new Dygraph(document.getElementById("graphdiv"),
          {{d.data|safe}},
          {
            labels: {{d.labels|safe}},
            axes: {
                x: {
                    valueFormatter: Dygraph.dateString_,
                    axisLabelFormatter: Dygraph.dateAxisFormatter,
                    ticker: Dygraph.dateTicker
                }
          },
          showRangeSelector: true,
          <!--labelsDivWidth:1600,-->
          legend: 'follow',
          labelsSeparateLines:true,
          connectSeparatedPoints:false
          });
