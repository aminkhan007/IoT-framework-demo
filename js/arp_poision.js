$("form").on('submit', function (e) {
    e.preventDefault();
 });
 function send_request()
 {
     var target_ip = $('#target_ip').val();
  
     var gateway_ip = $('#gateway_ip').val();
     var result1=null;
     var data = {"tip":target_ip,"gip":gateway_ip};
     $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: 'http://localhost:5000/arp_poision/',
        dataType : 'json',
        data : JSON.stringify(data),
        success : function(result) {
            console.log('I am in success')
            result1= result; 
        },error : function(result){
            text = result.responseText.split(',')
            var i;
        for (i = 0; i < text.length; i++) { 
        console.log(text[i]);
        }
            var i = 0;
            var b =0;
var element = document.getElementById("Result");
var interval = setInterval(function(){
         if(i <= text.length && b < text.length){
              element.innerHTML += text[b]+'\n';
              element.innerHTML+='<br>'
              }else{
            clearInterval(interval);
           }
        i++;
        b++;
 },1000);
            console.log(result.responseText)
        }
        });
        console.log(result1)
        
    }
