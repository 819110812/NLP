 $(document).ready(function() {
     $("#generate").click(function (event) {
         event.preventDefault();
         var text = $("#origins").val();
         var parm = $("#param").val();
         var score = $("#results").val();
         var data = {
                data: JSON.stringify({
                 'text': text,
                 'parm': parm,
                 'score': score
             }),
            };

         $.post({
             'url':'/summary/',
             'data':data,
              dataType: "json",
             'success':function (data) {
                 // alert("2")
                 console.log(data);
                 $("#results").html('sentence score:'+data['score']+'\n'+data['result']);
             },
             'error':function () {
                 alert("1");
             }

         })

     });

 });