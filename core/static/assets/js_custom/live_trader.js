    function changeColour(value) {
        var bg = document.getElementById("main_widget");
        switch(value)
        {
            case 'ask':
                bg.style.border = "solid 3px"
                bg.style.borderColor = "rgba(157, 237, 123, 0.60)";
                console.log(document.querySelector('input[name="side"]:checked').value,);
            break;
            case 'bid':
                bg.style.border = "solid 3px"
                bg.style.borderColor = "rgba(142, 47, 47, 0.60)";
                console.log(document.querySelector('input[name="side"]:checked').value,);
            break;
        }
    }

    let current_currency = document.getElementById('currency');

    console.log(current_currency.value);
    $('#price').val({{currency_data.USD}});

    {% for c, p in currency_data.items %}
        let {{c}} = {{p}};
    {% endfor %}

    var btc = '<i class="fa fa-bitcoin color-orange ml-1"></i>'
    var usdt = '<i class="fa fa-dollar text-success ml-1"></i>'
    var avg_priceIcon = $("#avg_price span.icon");
    var total_priceIcon = $("#total_price span.icon");
    var new_priceIcon = $("#new_price span.icon");
    var selectedExchange = $("#exchanges").val();

    $('#exchanges').change(function (event) {
        event.preventDefault();
        var selected = $(this).val();

        if (selected === "citex") {
            $('#pair').append($('<option>', {
                value: 'usdt',
                text: 'USD(T)',
                id: 'usdt'
            }))
        } else if (selected === "vitex"){
            $('#pair option[value=btc]').prop('selected', true).change();
            $('#usdt').remove();
        }
    });

    $(document).ready(function() {
        var at_start = $('#pair').val();

        var bg = document.getElementById("main_widget");

        bg.style.border = "solid 3px"
        bg.style.borderColor = "rgba(157, 237, 123, 0.60)";
        console.log(document.querySelector('input[name="side"]:checked').value,);

        if (selectedExchange === "vitex") {
            $('#usdt').remove();
        };

        if (at_start === "btc") {
                avg_priceIcon.html(btc);
                total_priceIcon.html(btc);
                new_priceIcon.html(btc);
            } else if (at_start === "usdt"){
                avg_priceIcon.html(usdt);
                new_priceIcon.html(usdt);
                total_priceIcon.html(usdt);
            };

        $('#pair').change(function (event) {
            event.preventDefault();
            var selected = $(this).val();

            if (selected === "btc") {
                avg_priceIcon.html(btc);
                total_priceIcon.html(btc);
                new_priceIcon.html(btc);
            } else if (selected === "usdt"){
                avg_priceIcon.html(usdt);
                new_priceIcon.html(usdt);
                total_priceIcon.html(usdt);
            }
        });
    });

    $('#currency').on('change', function (e) {
        e.preventDefault();
        console.log($(this).val())

        {% for c, p in currency_data.items %}
            if (current_currency.value === '{{c}}') {
                $('#price').val({{p}})
            }
         {% endfor %}
    });

    $(document).on('submit', '#orderbook-form',function(e){
        e.preventDefault();
        var csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type:'POST',
            url:'{% url "live_trader" %}',
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