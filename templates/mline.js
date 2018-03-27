<script>
  {% for l in d.mll %}
    $("#graphdiv").append('<div id = graphdiv'+{{l[0]|safe}}+'></div>');
    //alert(i);

    new Dygraph(document.getElementById("graphdiv"+{{l[0]|safe}}),
          {{l[2]|safe}},
          {
            labels: {{l[3]|safe}},
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
        
        //var annotations = [];
        //{% for item in d.y %}
        //annotations.push({
        //  series: {{item}},
        //  x: 1111017600000.0,
        //  shortText: x
        //});
        //{% endfor %}
        //
        //g.setAnnotations(annotations);
   {% endfor %}     
  $(function(){
  $('#tabs a[href="#tabs-2"]').click();
  //alert('#tabs a[href='+{{d.tab|safe}}+']');
  //$('#tabs a[href='+{{d.tab|safe}}+']').click();
  });

</script>

//<script>
//var g = new Dygraph(document.getElementById("graphdiv"),
//          {{d.data|safe}},
//          {
//            labels: {{d.labels|safe}},
//            axes: {
//                x: {
//                    valueFormatter: Dygraph.dateString_,
//                    axisLabelFormatter: Dygraph.dateAxisFormatter,
//                    ticker: Dygraph.dateTicker
//                }
//          },
//          showRangeSelector: true,
//          <!--labelsDivWidth:1600,-->
//          legend: 'follow',
//          labelsSeparateLines:true,
//          connectSeparatedPoints:false
//          });
//        
//        //var annotations = [];
//        //{% for item in d.y %}
//        //annotations.push({
//        //  series: {{item}},
//        //  x: 1111017600000.0,
//        //  shortText: x
//        //});
//        //{% endfor %}
//        //
//        //g.setAnnotations(annotations);
//        
//  $(function(){
//  $('#tabs a[href="#tabs-2"]').click();
//  //alert('#tabs a[href='+{{d.tab|safe}}+']');
//  //$('#tabs a[href='+{{d.tab|safe}}+']').click();
//  });
//
//</script>