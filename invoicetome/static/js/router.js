var app = app || {};

(function (app) {
  app.Router = Backbone.Router.extend({
    routes: {
      '': 'draft',
      'draft': 'draft',
      'sent': 'sent',
      'recieved': 'recieved',
      'share/:uuid': 'share',
    },

    draft: function () {
      console.log('draft');
      app.invoiceList.fire('filter', null, 'draft');
      $('.btn-draft').button('toggle');
    },

    sent: function () {
      console.log('sent');
      app.invoiceList.fire('filter', null, 'sent');
      $('.btn-sent').button('toggle');
    },

    recieved: function () {
      console.log('recieved');
      app.invoiceList.fire('filter', null, 'recieved');
      $('.btn-recieved').button('toggle');
    },

    share: function (uuid) {
      console.log('share', uuid);
    },
  });
  app.router = new app.Router();
  Backbone.history.start();
})(app);
