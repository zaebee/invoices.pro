from django_assets import Bundle, register

#Javascript
register('all_js',
        Bundle(
            'js/vendor/lodash.compat.min.js',
            'js/vendor/backbone-min.js',
            'js/vendor/ractive-legacy.min.js',
            'js/vendor/ractive-adaptors-backbone.js',
            'js/jquery.browser.min.js',
            'js/jquery.growfield2.js',
            'js/spin.min.js',
            'js/jquery.cookie.js',
            'js/jquery.spin.js',
            'js/bootstrap.min.js',
            'js/moment.min.js',
            'js/moment.ru.js',
            'js/app.js',
            'js/invoice.js',
            'js/task.js',
            'js/user.js',
            'js/utils.js',
        ),
        filters='jsmin',
        output='cache/packed.js')


register('pdf_js',
        Bundle(
            'js/vendor/lodash.compat.min.js',
            'js/vendor/backbone-min.js',
            'js/vendor/ractive-legacy.min.js',
            'js/vendor/ractive-adaptors-backbone.js',
            'js/jquery.browser.min.js',
            'js/jquery.growfield2.js',
            'js/spin.min.js',
            'js/jquery.cookie.js',
            'js/jquery.spin.js',
            'js/bootstrap.min.js',
            'js/moment.min.js',
            'js/moment.ru.js',
            #'js/app.js',
            #'js/invoice.js',
            #'js/task.js',
            #'js/user.js',
            #'js/utils.js',
        ),
        filters='jsmin',
        output='cache/packed.js')

#Css
register('all_css',
        Bundle(
               'css/bootstrap.min.css',
               'css/main.css',
        ),
        filters='cssmin',
        output='cache/packed.css')

