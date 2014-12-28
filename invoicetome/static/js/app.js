(function(){

  window.app = (function(){
    "use strict";
    var spinner_options = {
            lines: 11,
            length: 4,
            width: 2,
            radius: 3,
            trail: 60,
            speed: 1,
            shadow: false
        },

        buttonSpinner = function (button, button_text, spinner) {
            var _this = {};
            _this.button = button;
            _this.button_static_text = button.html();
            _this.button_spinning_text = button_text;
            _this.spinner = spinner;
            _this.start = function () {
                _this.button
                  .html(_this.button_spinning_text)
                  .addClass('disabled')
                  .prop('disabled', true);
                _this.spinner.spin(spinner_options);

            };
            _this.stop = function () {
                _this.button
                  .html(_this.button_static_text)
                  .removeClass('disabled')
                  .prop('disabled', false);
                _this.spinner.spin(false);
            };
            return _this;
        },

        show_success_message = function(message, fixed) {
          var msg = $('#success-message').clone().hide();
          if (fixed) {
            msg.addClass('fixed-block');
          } else {
            msg.removeClass('fixed-block');
          }
          msg.find('span').html(message);
          $('#message-placeholder').html(msg).find('.alert').fadeIn();
          setTimeout(function() {
            $('#message-placeholder').find('.alert-success').fadeOut();
          }, 3000);
        },

        show_failure_message = function (message, fixed) {
          var msg = $('#failure-message').clone().hide();
          if (fixed) {
            msg.addClass('fixed-block');
          } else {
            msg.removeClass('fixed-block');
          }
          msg.find('span').text(message);
          $('#message-placeholder').html(msg).find('.alert').fadeIn();
          setTimeout(function() {
            $('#message-placeholder').find('.alert-error').fadeOut();
          }, 3000);
        },

        api_request = function(options) {
          var url,
            _this = this;

          url = options.url;
          console.log(["" + options.type + " request to " + url + " with data:", options.data]);
          return $.ajax({
            url: url,
            type: options.type,
            dataType: options.dataType || 'json',
            processData: options.processData,
            contentType: options.contentType,
            data: options.data,
            beforeSend: function(xhr) {
              return xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            },
            success: function(response) {
              var params;

              console.log(['response from API: ', response]);
              if (options.successCallback) {
                params = [response];
                $.each(options.params || [], function(idx, p) {
                  return params.push(p);
                });
                return options.successCallback.apply(options.context, params);
              }
            }
          });
        };
    return {
      buttonSpinner: buttonSpinner,
      apiRequest: api_request,
      showSuccessMessage: show_success_message,
      showFailureMessage: show_failure_message,
    }

  }());

})();

(function (app) {

  var notes_top =
    "Dear Ms. Jane Doe,\n\n" +
    "\tPlease find below a cost-breakdown for the recent work completed. Please make payment at your earliest convenience, and do not hesitate to contact me with any questions.\n\r" +
    "\tMany thanks,\n" +
    "\tYour Name"

  var notes_bottom =
    "Many thanks for your custom! I look forward to doing business with you again in due course.\n\n" +
    "\tPayment terms: to be received within 60 days."


  app.User = Backbone.Model.extend({
    urlRoot: '/api/users/',
  });

  app.Invoice = Backbone.Model.extend({
    urlRoot: '/api/invoices/',
    idAttribute: 'uuid',
    defaults: {
      status: 'draft',
      company_name: gettext('Your Company Name'),
      address: gettext('123 Your Street'),
      city: gettext('Your Town'),
      address_second: gettext('Address Line 3'),
      phone: gettext('(123) 456 789'),
      email: USER.email || gettext('email@yourcompany.com'),
      invoice_name: gettext('Invoice'),
      invoice_uid: gettext('Invoice #') + _.random('10000'),
      invoice_po: gettext('PO 456001200'),
      client_name: gettext('Att: Ms. Jane Doe'),
      client_company: gettext('Client Company Name'),
      notes_top: gettext(notes_top),
      notes_bottom: gettext(notes_bottom),
      subtotal: 0,
      tax: 0,
      total: 0,
      headers: {
        h_description: gettext('Item Description'),
        h_quantity: gettext('Quantity'),
        h_unit_price: gettext('Unit Price (€)'),
        h_total: gettext('Total (€)'),
        subtotal: gettext('Subtotal'),
        tax: gettext('Sales tax (20%)'),
        total: gettext('Total'),
      },
    },
    sign: function (filename) {
      return app.apiRequest({
        url: '/api/sign/' + this.get('uuid') + '/',
        type: 'POST',
        data: {
          filename: filename,
        },
      });
    },
  });

  app.Invoices = Backbone.Collection.extend({
    url: '/api/invoices/',
    model: app.Invoice
  });

  app.Task = Backbone.Model.extend({
    urlRoot: '/api/tasks/',
  });

  app.Tasks = Backbone.Collection.extend({
    url: '/api/tasks/',
    model: app.Task
  });

  app.Spinner = function($el) {
    return new app.buttonSpinner($el, '&nbsp;', $el);
  };

})(app);


$(document).ready(function() {
  setTimeout(function(){
    $(".messages").fadeOut("slow");
  }, 4000 );
  $.ajaxSetup({
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
    }
  });
  $('[data-toggle=tooltip]').tooltip();
  $("textarea.notes").growfield();
});
