 var stripePublic_key =  $('#stripe_public_key').data('public_key');
        var clientSecret = $('#client_secret').data('secret');
        // var stripePublic_key = $('#id_stripe_public_key').text().slice(1, -1);
        // var clientSecret = $('#id_client_secret').text().slice(1, -1);
        var stripe = Stripe(stripePublic_key);


        // Set up Stripe.js and Elements to use in checkout form
        var elements = stripe.elements();
        var style = {
        base: {
            color: "#32325d",
        }
        };

        var card = elements.create("card", { style: style });
        card.mount("#card-element");

        card.on('change', function(event) {
            var displayError = document.getElementById('card-errors');
            if (event.error) {
                var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${event.error.message}</span>
                `;
                $(errorDiv).html(html);
            } else {
                displayError.textContent = '';
            }
        });

    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
        card: card,
        billing_details: {
            name: $.trim(form.full_name.value),
            phone: $.trim(form.phone_number.value),
            email: $.trim(form.email.value),
            address:{
                line1: $.trim(form.address_1.value),
                line2: $.trim(form.address_2.value),
                city: $.trim(form.city.value),
                country: $.trim(form.country.value),
                state: $.trim(form.state.value),
                postal_code: $.trim(form.postcode.value),
            }
        }
        },
        shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.address_1.value),
                    line2: $.trim(form.address_2.value),
                    city: $.trim(form.city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.state.value),
                }
        },
    }).then(function(result) {
        if (result.error) {
        // Show error to your customer (e.g., insufficient funds)
        console.log(result.error.message);
        } else {
        // The payment has been processed!
        if (result.paymentIntent.status === 'succeeded') {
            form.submit();
            // Show a success message to your customer
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
        }
        }
    });
    });