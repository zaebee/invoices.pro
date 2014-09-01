var app = app || {};

(function (app) {

  app.invoice = new Ractive({
    el: '#invoice',
    template: '#invoice-template',
    data: {
      invoice: new app.Invoice, // наша Backbone модель

      date: function () {
          return new Date();
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
    adaptors: [ Ractive.adaptors.Backbone ],
  });

  app.invoice.on({
    save: function(event) {
      event.preventDefault();
      var spinner = new app.buttonSpinner(
        $('#save-invoice'),
        '&nbsp;',
        $('#save-invoice')
      );
      spinner.start();

      var tasks = app.tasks.get('tasks').filter(function(el){
        return el.get('description');
      }).map(function(el){
        return el.toJSON();
      });
      this.set('invoice.records', tasks);
      this.get('invoice').save(null, {
        success: function(model, response) {
          spinner.stop();
        },
      });
    },

    generate_pdf: function(event) {
      event.preventDefault();
      var spinner = new app.buttonSpinner($('#get-pdf'), '&nbsp;', $('#get-pdf'));
      spinner.start();
      setTimeout(function(){
        spinner.stop();
      },3000);
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

  $("textarea.notes").growfield();
  // сразу сохраняем инвойс на сервер
  //app.invoice.data.invoice.save();

})(app);
