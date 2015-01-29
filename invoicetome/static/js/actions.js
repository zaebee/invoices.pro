var app = app || {};

(function (app) {

  app.actions = new Ractive({
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
      status: 'draft',
    },
    adapt: [ Ractive.adaptors.Backbone ],
  });

  app.actions.on({
    //***
    //
    //***
    new: function( event ) {
      event.original.preventDefault();
      console.log(event.context);
      return;
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
      _.each(_.range(8), function(){
        tasks.add(new app.Task(params));
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
          $('.actions-nav.in').offcanvas('hide');
        },
      });
    },

    //***
    //
    //***
    copy: function( event ) {
      event.original.preventDefault();
      var invoice = app.invoice.get('invoice').clone();
      var spinner = app.Spinner($('#copy-invoice'));
      spinner.start();
      invoice.unset('id');
      invoice.unset('uuid');
      invoice.unset('status');
      invoice.unset('histories');
      invoice.unset('recipient_email');
      invoice.unset('signed');
      invoice.unset('signature_id');
      invoice.unset('signature_request_id');
      invoice.save(null, {
        success: function(model, response) {
          if ($('[name=options]:checked').val() == 'draft') {
            app.invoiceList.get('invoices').add(model, {at:0});
            app.invoiceList.fire('activate');
          };
          app.showSuccessMessage(gettext('Invoice copied and saved in draft.'));
          spinner.stop();
          $('.actions-nav.in').offcanvas('hide');
        },
      });
    },

    //***
    //
    //***
    delete: function( event ) {
      event.original.preventDefault();
      var spinner = app.Spinner($('#delete-invoice'));
      spinner.start();
      app.invoice.get('invoice').destroy({
        success: function(model, response) {
          app.showSuccessMessage(gettext('Invoice was deleted.'));
          spinner.stop();
          $('.actions-nav.in').offcanvas('hide');
          app.invoiceList.fire('activate');
        },
      });
    },

    //***
    //
    //***
    save: function( event ) {
      event.original.preventDefault();
      var spinner = app.Spinner($('#save-invoice'));
      spinner.start();
      var tasks = app.tasks.get('tasks').toJSON();
      app.invoice.set('invoice.records', tasks);
      app.invoice.get('invoice').save(null, {
        success: function(model, response) {
          app.invoiceList.get('invoices').add(model, {at: 0});
          var tasks = model.get('records');
          tasks = new app.Tasks(tasks);
          app.tasks.set('tasks', tasks);
          app.showSuccessMessage(gettext('Invoice was saved.'));
          spinner.stop();
          $('.actions-nav.in').offcanvas('hide');
        },
      });
    },

    //***
    //
    //***
    send: function( event ) {
      event.original.preventDefault();
      var $client_email = $('[name=client_email]');
      if ($client_email.length) {
        var email = $client_email.val();
        if (email) {
          var spinner = app.Spinner($('#send-invoice'));
          spinner.start();
          var tasks = app.tasks.get('tasks').toJSON();
          app.invoice.set('invoice.records', tasks);
          app.invoice.set('invoice.recipient_email', email);
          app.invoice.get('invoice').save(null, {
            success: function (model, response) {
              app.invoiceList.get('invoices').remove(model);
              var tasks = model.get('records');
              tasks = new app.Tasks(tasks);
              app.tasks.set('tasks', tasks);
              $('[data-toggle=popover]').popover('hide');
              app.showSuccessMessage(gettext('Invoice sent success to ') + email);
              spinner.stop();
              $('.actions-nav.in').offcanvas('hide');
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
      event.original.preventDefault();
      app.makeMarkup();
      var spinner = app.Spinner($('#get-pdf'));
      spinner.start();
      var tasks = app.tasks.get('tasks').toJSON();
      app.invoice.set('invoice.records', tasks);
      app.invoice.get('invoice').save(null, {
        success: function (model, response) {
          spinner.stop();
          if (app.invoice.get('invoice.signed')) {
            document.location.pathname = '/api/pdf/' + app.invoice.get('invoice.uuid');
          } else {
            $(app.invoice.el).parents('form').submit();
          };
          if (!app.invoice.get('user').authenticated) {
            app.router.navigate('/', {trigger:true});
          }
        },
      });
      $('.actions-nav.in').offcanvas('hide');
    },

  });

  app.invoice.observe('invoice.uuid invoice.disabled', function(val, old, keypath){
    app.actions.set('invoice', app.invoice.get('invoice'));
  });

})(app);
