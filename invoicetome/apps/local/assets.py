from django_assets import Bundle, register

#Javascript
register('all_js',
        Bundle(
            #'js/page.js',
            'js/vendor/lodash.compat.min.js',
            'js/vendor/backbone-min.js',
            'js/vendor/ractive-legacy.min.js',
            'js/vendor/ractive-adaptors-backbone.js',
            'js/jquery.browser.min.js',
            'js/jquery.growfield2.js',
            'js/textsaver.js',
            'js/spin.min.js',
            'js/jquery.spin.js',
            'js/bootstrap.min.js',
            'js/app.js',
            'js/invoice.js',
            'js/task.js',
            'js/user.js',
        ),
        filters='jsmin',
        output='cache/packed.js')

#Css
register('all_css',
        Bundle(
               'css/bootstrap.min.css',
               'css/app.css',
               'css/main.css',
        ),
        filters='cssmin',
        output='cache/packed.css')

