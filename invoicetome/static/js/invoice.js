var app = app || {};

(function (app) {

  app.invoiceList = new Ractive({
    el: '#invoice-list .list-group',
    template: '#invoice-list-template',
    data: {
      invoices: new app.Invoices(), // наша Backbone модель
      user: USER,
      status: {
        draft: gettext('Draft Invoices'),
        sent: gettext('Sent Invoices'),
        recieved: gettext('Recieved Invoices'),
      },
      title: function (recipient) {
        if (recipient) {
          return gettext('Sent to ') + recipient;
        } else {
          return '';
        } 
      },
      date_short: function (date) {
        var date = new Date(date);
        var date = moment(date);
        return date.lang('en').format('DD.MM.YYYY HH:mm');
      },

    },
    adaptors: [ Ractive.adaptors.Backbone ],
  });

  app.invoice = new Ractive({
    el: '#invoice-detail',
    template: '#invoice-template',
    data: {
      text: {
        history_title: gettext('Invoice History'),
      },
      user: USER,
      invoice: new app.Invoice, // наша Backbone модель

      date: function () {
        var date = this.get('invoice.date_added') || new Date();
        var date = moment(date);
        return date.lang('en').format('DD MMMM YYYY');
      },
      history_date: function (date) {
        var date = new Date(date);
        var date = moment(date);
        return date.lang('en').format('DD MMMM YYYY HH:mm');
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

  app.aside = new Ractive({
    el: '#actions-bar',
    template: '#invoice-actions-template',
    data: {
      text: {
        status: {
          draft: gettext('Draft Invoices'),
          sent: gettext('Sent Invoices'),
          recieved: gettext('Recieved Invoices'),
        },
        create_new: gettext('Create New'),
        get_pdf: gettext('Get Pdf'),
        get_share_link: gettext('Get Share Link'),
        copy: gettext('Copy'),
        save: gettext('Save'),
        send: gettext('Send'),
        delete: gettext('Delete'),
        resize_table: gettext('Resize Table'),
        add_row: gettext('Add Row'),
        delete_row: gettext('Delete Row'),
        finished: gettext('Finished editing?'),
      },
      user: USER,
      invoice: app.invoice.get('invoice'),
      status: 'draft',
    },
    adaptors: [ Ractive.adaptors.Backbone ],
  });


  app.invoiceList.on({
    activate: function (event ) {
      if (event) {
        event.original.preventDefault();
        $(event.node).siblings().removeClass('active');
        $(event.node).addClass('active');
        var invoice = event.context;
      } else {
        var invoice = this.get('invoices').at(0);
        if (!invoice) return;
        var $node = $('[data-uuid=' + invoice.get('uuid') + ']');
        $node.siblings().removeClass('active');
        $node.addClass('active');
      };
      app.invoice.set('invoice', invoice);
      var tasks = invoice.get('records');
      tasks = new app.Tasks(tasks);
      app.tasks.set('tasks', tasks);
      app.router.navigate(invoice.get('status') + '/' + invoice.get('uuid'));
      $(".notes:not(.growfieldDummy)").growfield('restart');
    },
    share: function( event ) {
      event.original.preventDefault();
      event.original.stopPropagation();
      var invoice = event.context;
      console.log('share');
    },
    delete: function( event ) {
      event.original.preventDefault();
      event.original.stopPropagation();
      var invoice = event.context;
      var spinner = app.Spinner($('#delete-invoice'));
      spinner.start();
      invoice.destroy({
        success: function(model, response) {
          app.showSuccessMessage(gettext('Invoice was deleted.'));
          spinner.stop();
          app.invoiceList.fire('activate');
        },
      });
    },
  });

  app.invoice.on({
    //***
    //
    //***
    new: function( event ) {
      var spinner = app.Spinner($('#new-invoice'));
      spinner.start();
      var invoice = new app.Invoice();
      var params = {
        description: '',
        quantity: 0,
        unit_price: 0,
        total: 0,
      };
      var tasks = new app.Tasks();
      _.each(_.range(8), function(el){
        var task = new app.Task(params);
        tasks.add(task);
      });

      var tasks = tasks.toJSON();
      invoice.set('records', tasks);

      invoice.save(null, {
        success: function(model, response) {
          if ($('[name=options]:checked').val() == 'draft') {
            app.invoiceList.get('invoices').add(model, {at: 0});
            app.invoiceList.fire('activate');
          };
          app.showSuccessMessage(gettext('New Invoice was saved in draft.'));
          spinner.stop();
        },
      });
    },

    //***
    //
    //***
    copy: function( event ) {
      var invoice = app.invoice.get('invoice').clone();
      var spinner = app.Spinner($('#copy-invoice'));
      spinner.start();
      invoice.id = null;
      invoice.unset('id');
      invoice.unset('uuid');
      invoice.unset('status');
      invoice.unset('histories');
      invoice.unset('recipient_email');
      invoice.save(null, {
        success: function(model, response) {
          if ($('[name=options]:checked').val() == 'draft') {
            app.invoiceList.get('invoices').add(model, {at:0});
            app.invoiceList.fire('activate');
          };
          app.showSuccessMessage(gettext('Invoice copied and saved in draft.'));
          spinner.stop();
        },
      });
    },

    //***
    //
    //***
    delete: function( event ) {
      var spinner = app.Spinner($('#delete-invoice'));
      spinner.start();
      this.get('invoice').destroy({
        success: function(model, response) {
          app.showSuccessMessage(gettext('Invoice was deleted.'));
          spinner.stop();
          app.invoiceList.fire('activate');
        },
      });
    },

    //***
    //
    //***
    save: function( event ) {
      var spinner = app.Spinner($('#save-invoice'));
      spinner.start();
      var tasks = app.tasks.get('tasks').toJSON();
      this.set('invoice.records', tasks);
      this.get('invoice').save(null, {
        success: function(model, response) {
          app.invoiceList.get('invoices').add(model, {at: 0});
          var tasks = model.get('records');
          tasks = new app.Tasks(tasks);
          app.tasks.set('tasks', tasks);
          app.showSuccessMessage(gettext('Invoice was saved.'));
          spinner.stop();
        },
      });
    },

    //***
    //
    //***
    send: function( event ) {
      console.log('fired send');
      var $client_email = $('[name=client_email]');
      if ($client_email.length) {
        var email = $client_email.val();
        if (email) {
          var spinner = app.Spinner($('#send-invoice'));
          spinner.start();
          var tasks = app.tasks.get('tasks').toJSON();
          this.set('invoice.records', tasks);
          this.set('invoice.recipient_email', email);
          this.get('invoice').save(null, {
            success: function (model, response) {
              app.invoiceList.get('invoices').remove(model);
              var tasks = model.get('records');
              tasks = new app.Tasks(tasks);
              app.tasks.set('tasks', tasks);
              $('[data-toggle=popover]').popover('hide');
              app.showSuccessMessage(gettext('Invoice sent success to ') + email);
              spinner.stop();
              app.invoiceList.fire('activate');
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

    //***
    //
    //***
    generate_pdf: function( event ) {
      app.makeMarkup();
      $(app.invoice.el).parents('form').submit();
    },
  });

  app.aside.on({
    filter: function( event, status ) {
      app.router.navigate(status);
      app.aside.set('status', status);
      if (status == 'recieved') {
        var data = {
          recipient_email: this.get('user.email'),
        };
      } else {
        var data = {
          status: status,
        };
      }
      app.aside.set('active_status', app.invoiceList.get('status')[status]);
      app.invoiceList.get('invoices').fetch({
        data: data,
        success: function () {
          $('.nano').nanoScroller();
          app.invoiceList.fire('activate');
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
