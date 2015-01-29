var app = app || {};

(function (app) {

  app.invoiceList = new Ractive({
    el: '#invoice-list .list-group',
    template: '#invoice-list-template',
    data: {
      invoices: new app.Invoices(),
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
        return date.lang(USER.lang).format('DD.MM.YYYY HH:mm');
      },

    },
    adapt: [ Ractive.adaptors.Backbone ],
  });


  app.invoiceList.on({
    activate: function (event ) {
      if (event) {
        event.original.preventDefault();
        $(event.node).siblings().removeClass('active');
        $(event.node).addClass('active');
        var invoice = event.context;
        $('#invoice-list-collapse.in').offcanvas('hide');
      } else {
        var invoice = this.get('invoices').at(0);
        if (!invoice) {
          app.router.init_tasks();
          return;
        };
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
          $('#invoice-list-collapse.in').offcanvas('hide');
          app.invoiceList.fire('activate');
        },
      });
    },
  });

})(app);
