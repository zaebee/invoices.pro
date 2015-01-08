var app = app || {};

(function (app) {

  app.profile = new Ractive({
    el: '#profileModal',
    template: '#profile-template',
    data: {
      user: new app.User(USER), // наша Backbone модель
    },
    adapt: [ Ractive.adaptors.Backbone ],
  });


  app.profile.on({
    save: function(event) {
      var $node = $(event.node);
      var user = event.context.user;
      var spinner = app.Spinner($node);
      spinner.start();
      user.save(null, {
        success: function(model, response) {
          spinner.stop();
          $('#profileModal').modal('hide');
          app.showSuccessMessage(gettext('Profile saved.'));
        },
      });
    },
  });

})(app);
