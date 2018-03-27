    var g = new Dygraph(document.getElementById("graphdiv1"),
              [
                [1,10,100],
                [2,20,80],
                [3,50,60],
                [4,70,80]
              ],
              {
                labels: [ "x", "A", "B" ],
                //fractions: true,
                //errorBars: true,
                //showRangeSelector: true,
                valueRange: [20, 100],
                showRoller: true,
                rollPeriod: 15
              });