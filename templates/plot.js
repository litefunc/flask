<script>
//$(document).ready(function(){
  //var i = 1;
  //$("#div7 input").click(function(){
    $("#div9").append('<div id = graphdiv'+{{d.i}}+'></div>');
    //alert(i);
    
    new Dygraph(document.getElementById("graphdiv"+{{d.i}}),
              {{d.data1|safe}},
              {
                labels: {{d.labels1|safe}},
                axes: {
                    x: {
                        valueFormatter: Dygraph.dateString_,
                        axisLabelFormatter: Dygraph.dateAxisFormatter,
                        ticker: Dygraph.dateTicker
                    }
              },
              showRangeSelector: true,
              legend: 'follow',
              labelsSeparateLines:true,
              connectSeparatedPoints:false
              });
    //$('body').append('<div id = graphdiv'+i+'></div>');
    
              //new Dygraph(document.getElementById("graphdiv"+i),
              //  [
              //    [1,10,100],
              //    [2,20,80],
              //    [3,50,60],
              //    [4,70,80]
              //  ],
              //  {
              //    labels: [ "x", "A", "B" ],
              //    showRangeSelector: true,
              //    valueRange: [20, 100],
              //    showRoller: true,
              //    rollPeriod: 15
              //  });
      //$('#graphdiv'+i).append(i);
      //i+=1;      
      $( function(){
        $('#tabs a[href="#tabs-3"]').click();
      });
  //});  
//});  
  
</script>

