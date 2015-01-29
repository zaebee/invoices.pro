var app = app || {};

(function (app) {

  app.invoice = new Ractive({
    el: '#invoice-detail',
    template: '#invoice-template',
    data: {
      text: {
        history_title: gettext('Invoice History'),
      },
      user: USER,
      invoice: new app.Invoice,

      date: function () {
        var date = this.get('invoice.date_added') || new Date();
        var date = moment(date);
        return date.lang(USER.lang).format('DD MMMM YYYY');
      },
      history_date: function (date) {
        var date = new Date(date);
        var date = moment(date);
        return date.lang(USER.lang).format('DD MMMM YYYY HH:mm');
      },
      // хэлпер используется в шаблоне {{ format(price) }}
      format: function ( num ) {
        return parseFloat(num).toFixed( 2 );
      },

      set_total: function(tax_percent) {
        var subtotal = this.invoice.get('subtotal');
        var tax = this.invoice.get('subtotal') * tax_percent;
        this.invoice.set('tax', tax);
        this.invoice.set('total', parseFloat(subtotal) + parseFloat(tax));
      }
    },
    adapt: [ Ractive.adaptors.Backbone ],
  });


  app.invoice.on({

    //***
    //
    //***
    sign: function( event ) {
      event.original.preventDefault();
      event.original.stopPropagation();
      var invoice = event.context;
      var spinner = app.Spinner($('#sign-invoice-spinner'));
      spinner.start();
      app.makeMarkup();
      app.apiRequest({
        url: '/generate_pdf.php',
        type: 'POST',
        data : {
          html: $('#markup').val(),
          file: true,
        },
        successCallback: function(response) {
          if (response.created) {
            invoice.sign(response.filename).done(function (response) {
              spinner.stop();
              if (!response.sign_url) {
                spinner.stop();
                app.showFailureMessage(gettext('PDF file wasn\'t created.'));
                return;
              };
              HelloSign.open({
                skipDomainVerification: true,
                url: response.sign_url,
                allowCancel: true,
                container: document.getElementById('sign-container'),
                messageListener: function(eventData) {
                  console.log(eventData);
                  if (eventData.event == HelloSign.EVENT_SIGNED) {
                    app.invoice.set('invoice.signed', true);
                    app.invoice.set('invoice.disabled', true);
                    invoice.save();
                    $('#sign-container-wrapper').addClass('hide');
                  };
                }
              });
              $('#sign-container-wrapper').removeClass('hide');
            });
          } else {
            spinner.stop();
            app.showFailureMessage(gettext('PDF file wasn\'t created.'));
          }
        },
      });
    },
  });


  app.invoice.observe('invoice.headers.tax', function(tax, old, keypath){
    var tax_percent = tax.replace(/\,/g, '').replace(/,/g,'.').replace(/[^\d\.]/g,'') / 100;
    this.data.set_total(tax_percent);
  });
  app.invoice.observe('invoice.subtotal', function(subtotal, old, keypath){
    var tax_percent = this.get('invoice.headers.tax').replace(/\,/g, '').replace(/,/g,'.').replace(/[^\d\.]/g,'') / 100;
    this.data.set_total(tax_percent);
  });

})(app);
