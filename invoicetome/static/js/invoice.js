var app = app || {};

(function (app) {

  app.invoiceList = new Ractive({
    el: '#invoice-list .list-group',
    template: '#invoice-list-template',
    data: {
      invoices: new app.Invoices(), // наша Backbone модель
      user: USER,
      status: {
        draft: gettext('Draft'),
        sended: gettext('Sent'),
        recieved: gettext('Recieved'),
      },
      title: function (recipient) {
        if (recipient) {
          return gettext('Sent to ') + recipient;
        } else {
          return '';
        } 
      },
    },
    adaptors: [ Ractive.adaptors.Backbone ],
  });

  app.invoice = new Ractive({
    el: '#invoice',
    template: '#invoice-template',
    data: {
      user: USER,
      invoice: new app.Invoice, // наша Backbone модель

      date: function () {
        var date = this.get('invoice.date_added') || new Date();
        var date = moment(date);
        return date.lang('en').format('DD MMMM YYYY');
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

  app.invoiceList.on({
    activate: function(event) {
      event.original.preventDefault();
      $(event.node).addClass('active');
      $(event.node).siblings().removeClass('active');
      app.invoice.set('invoice', event.context);
      var tasks = event.context.get('records');
      tasks = new app.Tasks(tasks);
      app.tasks.set('tasks', tasks);
    },
    filter: function(event, status) {
      console.log(event, status);
      $(event.node).parent().siblings().find('.btn').removeClass('active');
      $(event.node).addClass('active');
      if (status == 'recieved') {
        var data = {
          recipient_email: this.get('user.email'),
        };
        console.log(data);
      } else {
        var data = {
          status: status,
        };
      }
      this.get('invoices').fetch({
        data: data,
      });
    },
  });

  app.invoice.on({
    save: function( event ) {
      app.saveSpinner.start();

      var tasks = app.tasks.get('tasks').toJSON();
      this.set('invoice.records', tasks);
      this.get('invoice').save(null, {
        success: function(model, response) {
          app.invoiceList.get('invoices').add(model);
          var tasks = model.get('records');
          tasks = new app.Tasks(tasks);
          app.tasks.set('tasks', tasks);
          app.saveSpinner.stop();
        },
      });
    },

    send: function( event ) {
      console.log('fired send');
      var $client_email = $('[name=client_email]');
      if ($client_email.length) {
        var email = $client_email.val();
        if (email) {
          app.sendSpinner.start();
          var tasks = app.tasks.get('tasks').toJSON();
          this.set('invoice.records', tasks);
          this.set('invoice.recipient_email', email);
          this.get('invoice').save(null, {
            success: function (model, response) {
              app.invoiceList.get('invoices').add(model);
              var tasks = model.get('records');
              tasks = new app.Tasks(tasks);
              app.tasks.set('tasks', tasks);
              app.sendSpinner.stop();
              $('[data-toggle=popover]').popover('hide');
            },
          });
        } else {
          $('[data-toggle=popover]').popover('hide');
        }
      } else {
        $('[data-toggle=popover]').popover('show');
	$client_email.focus();
      }
    },

    generate_pdf: function( event ) {
      app.pdfSpinner.start();
      var tasks = app.tasks.get('tasks').toJSON();
      this.set('invoice.records', tasks);
      this.get('invoice').save(null, {
        success: function (model, response) {
          app.invoiceList.get('invoices').add(model);
          var tasks = model.get('records');
          tasks = new app.Tasks(tasks);
          app.tasks.set('tasks', tasks);
          app.pdfSpinner.stop();
          app.makeMarkup();
          $(app.invoice.el).parent('form').submit();
        }
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

  $("textarea.notes").growfield();
  app.invoiceList.get('invoices').fetch({
    data: {
      status: 'draft'
    }
  });

})(app);
