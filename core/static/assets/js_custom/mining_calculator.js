$(document).on('submit', '#orderbook-form',function(e){
        e.preventDefault();
        var csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type:'POST',
            url:'{% url "orderbook" %}',
            data:{
                quantity:$('#quantity').val(),
                exchange:$('#exchanges').val(),
                pair:$('#pair').val(),
                side: document.querySelector('input[name="side"]:checked').value,
                csrfmiddlewaretoken: csrf,
                action: 'post-orderbook'
            },
            success:function(json) {
                $('#avg_price span.num').text(json.average)
<!--                $('#avg_price span.to_usd').html('-->
<!--                    <i class="fa fa-dollar dollar-color"></i>-->
<!--                    <span class="h5  text-white">' + json.average + '</span>')-->
                $('#total_price span.num').text(json.total)
                $('#new_price span.num').text(json.new_price)
                $('#price_impact').text('Price impact: ' + json.impact.toFixed(2) + '%')
            },
            error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });