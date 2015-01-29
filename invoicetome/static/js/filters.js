var app = app || {};

(function (app) {

  app.filters = new Ractive({
    el: '.invoice-list-filter',
    template: '#invoice-list-filter-template',
    data: {
      text: {
        status: {
          draft: gettext('Draft Invoices'),
          sent: gettext('Sent Invoices'),
          recieved: gettext('Recieved Invoices'),
        },
      },
      user: USER,
      invoice: app.invoice.get('invoice'),
      status: 'draft',
    },
    adapt: [ Ractive.adaptors.Backbone ],
  });

  app.filters.on({
    filter: function( event, status ) {
      var list = $('#invoice-list').spin();
      list.find('.nano').hide();
      app.router.navigate(status);
      app.actions.set('status', status);
      if (status == 'recieved') {
        var data = {
          recipient_email: this.get('user.email'),
        };
      } else {
        var data = {
          status: status,
        };
      }
      app.filters.set('active_status', app.invoiceList.get('status')[status]);
      app.invoiceList.get('invoices').fetch({
        data: data,
        reset: true,
        success: function () {
          list.data('spinner').stop();
          list.find('.nano').show();
          $('.nano').nanoScroller();
          app.invoiceList.fire('activate');
        },
      });
    },
  });

})(app);
