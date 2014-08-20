from django_assets import Bundle, register

#Javascript
register('all_js',
        Bundle(
            #'js/page.js',
            'js/jquery.browser.min.js',
            'js/jquery.growfield2.js',
            'js/textsaver.js',
            'js/bootstrap.min.js',
        ),
        filters='jsmin',
        output='cache/packed.js')

#Css
register('all_css',
        Bundle(
               #'css/bootstrap.min.css',
               'css/app.css',
               'css/main.css',
        ),
        filters='cssmin',
        output='cache/packed.css')

