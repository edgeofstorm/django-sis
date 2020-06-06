$(document).ready(function () {
    $("#option2").click(function(){
        $("#myChart2").css('display','none')
        $("#myChart3").css('display','block')
      });
      $("#option1").click(function(){
        $("#myChart3").css('display','none')
        $("#myChart2").css('display','block')
      });
    //   $("#chart-type-option1").click(function(){
    //     $("#myChart2-line").css('display','none')
    //     $("#myChart3-line").css('display','block')
    //   });
    //   $("#chart-type-option2").click(function(){
    //     $("#myChart2").css('display','none')
    //     $("#myChart3").css('display','block')
    //   });
});

// new Chart(document.getElementById("myChart2"), { 
//     "type": "line",
//     "data": { 
//         "labels": [{% for exam_result in exams_all %}'{{exam_result.exam.title}},{{exam_result.exam.timestamp|date:"d M Y"}}',{% endfor %}],
//         "datasets": [
//                 { 
//                     "label": "Net Sayisi",
//                     "data": [{% for exam_result in exams_all %}'{{ exam_result.result.Net }}', {% endfor %}],
//                     "fill": false,
//                     "borderColor": "rgb(75, 192, 192)",
//                     "lineTension": 0.1
//                 },
//                 {
//                     "label": "Matematik Net",
//                     "data": [{% for exam_result in exams_all %}'{{ exam_result.result.Yanlis.M }}', {% endfor %}],
//                     "fill": false,
//                     "borderColor": "rgb(75, 255, 192)",
//                     "lineTension": 0.1
//                 }
//             ]
//         },
//     "options": { responsive: true, scales: { yAxes: [{ ticks: { min: 50, max: 80 } }] } }});