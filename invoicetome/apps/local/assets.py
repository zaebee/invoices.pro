from django_assets import Bundle, register

#Javascript
register('all_js',
        Bundle(
            'js/vendor/lodash.compat.min.js',
            'js/vendor/backbone-min.js',
            'js/vendor/ractive.js',
            'js/vendor/ractive-adaptors-backbone.js',
            'js/vendor/moment.min.js',
            'js/vendor/moment.ru.js',
            'js/vendor/jquery.browser.min.js',
            'js/vendor/jquery.growfield2.js',
            'js/vendor/jquery.nanoscroller.min.js',
            'js/vendor/spin.min.js',
            'js/vendor/jquery.cookie.js',
            'js/vendor/jquery.spin.js',
            'js/vendor/bootstrap.min.js',
            'js/vendor/jasny-bootstrap.js',

            'js/app.js',
            'js/utils.js',
            'js/invoice.js',
            'js/task.js',
            'js/profiles.js',

            'js/router.js',
        ),
        filters='jsmin',
        output='cache/packed.js')


register('pdf_js',
        Bundle(
            'js/vendor/lodash.compat.min.js',
            'js/vendor/backbone-min.js',
            'js/vendor/ractive.js',
            'js/vendor/ractive-adaptors-backbone.js',
            'js/vendor/moment.min.js',
            'js/vendor/moment.ru.js',
            'js/vendor/jquery.browser.min.js',
            'js/vendor/jquery.growfield2.js',
            'js/vendor/jquery.nanoscroller.min.js',
            'js/vendor/spin.min.js',
            'js/vendor/jquery.cookie.js',
            'js/vendor/jquery.spin.js',
            'js/vendor/bootstrap.min.js',
            'js/vendor/jasny-bootstrap.js',

            'js/app.js',
            #'js/invoice.js',
            #'js/task.js',
            'js/profiles.js',
            'js/utils.js',
        ),
        filters='jsmin',
        output='cache/packed.js')

#Css
register('all_css',
        Bundle(
               'css/bootstrap.min.css',
               'css/jasny-bootstrap.css',
               'css/nanoscroller.css',
               'css/main.css',
        ),
        filters='cssmin',
        output='cache/packed.css')

