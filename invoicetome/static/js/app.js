(function(){

  window.App = (function(){
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
          var msg = $('#success-message').clone();
          if (fixed) {
            msg.addClass('fixed-block');
          } else {
            msg.removeClass('fixed-block');
          }
          msg.find('span').html(message);
          $('#message-placeholder').html(msg);
        },

        show_failure_message = function (message, fixed) {
          var msg = $('#failure-message').clone();
          if (fixed) {
            msg.addClass('fixed-block');
          } else {
            msg.removeClass('fixed-block');
          }
          msg.find('span').text(message);
          $('#message-placeholder').html(msg);
        },

        show_info_message = function (message, fixed) {
          var msg = $('#info-message').clone();
          if (fixed) {
            msg.addClass('fixed-block');
          } else {
            msg.removeClass('fixed-block');
          }
          msg.find('span').text(message);
          $('#message-placeholder').html(msg);
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
      showInfoMessage: show_info_message,
    }

  }());


})();
