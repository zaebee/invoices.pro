var app = app || {};

(function (app) {
  app.Router = Backbone.Router.extend({
    routes: {
      '': 'draft',
      ':status/:uuid': 'detail',
      'draft': 'draft',
      'sent': 'sent',
      'recieved': 'recieved',
    },

    init_tasks: function () {
      // Добавляем первый заполненный таск и 7 пустых
      var invoice = new app.Invoice();
      app.invoice.set('invoice', invoice);
      app.tasks.get('tasks').reset();
      app.tasks.fire('add', {first: true});
      _.each(_.range(7), function(el){
        app.tasks.fire('add');
      });

      var tasks = app.tasks.get('tasks').toJSON();
      app.invoice.set('invoice.records', tasks);
    },

    draft: function () {
      this.init_tasks();
      console.log('draft');
      app.aside.fire('filter', null, 'draft');
      $('.btn-draft').button('toggle');
    },

    sent: function () {
      this.init_tasks();
      app.aside.fire('filter', null, 'sent');
      $('.btn-sent').button('toggle');
    },

    recieved: function () {
      this.init_tasks();
      app.aside.fire('filter', null, 'recieved');
      $('.btn-recieved').button('toggle');
    },

    detail: function (status, uuid) {
      app.invoice.set('invoice.uuid', uuid);
      app.invoice.get('invoice').fetch({
        success: function(model, response) {
          var tasks = model.get('records');
          tasks = new app.Tasks(tasks);
          app.tasks.set('tasks', tasks);
          app.aside.set('status', status);
          app.aside.set('active_status', app.invoiceList.get('status')[status]);
          $('.btn-' + status).button('toggle');
          app.invoiceList.get('invoices').fetch({
            data: {
              status: status,
            },
            success: function() {
              $('[data-uuid=' + uuid + ']').addClass('active');
              $('.nano').nanoScroller();
              $(".notes:not(.growfieldDummy)").growfield('restart');
            },
          });
        },
      });
      console.log('detail', uuid);
    },
  });
  $('#company').focus();
  app.router = new app.Router();
  Backbone.history.start();
})(app);
