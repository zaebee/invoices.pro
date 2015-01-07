var app = app || {};

(function (app) {

  app.profile = new Ractive({
    el: '#profile-detail',
    template: '#profile-template',
    data: {
      user: new app.User(USER), // наша Backbone модель

    },
    adapt: [ Ractive.adaptors.Backbone ],
  });


  app.profile.on({
  });


})(app);
