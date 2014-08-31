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
        return num.toFixed( 2 );
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

  app.invoice.observe('invoice.headers.tax', function(tax, old, keypath){
    var tax_percent = tax.replace(/\,/g, '').replace(/,/g,'.').replace(/[^\d\.]/g,'') / 100;
    this.data.set_total(tax_percent);
  });
  app.invoice.observe('invoice.subtotal', function(subtotal, old, keypath){
    var tax_percent = this.get('invoice.headers.tax').replace(/\,/g, '').replace(/,/g,'.').replace(/[^\d\.]/g,'') / 100;
    this.data.set_total(tax_percent);
  });

  // сразу сохраняем инвойс на сервер
  $("textarea.notes").growfield();
  //app.invoice.data.invoice.save();

})(app);
