from django_assets import Bundle, register

#Javascript
register('all_js',
        Bundle(
            'js/app.js',
            'js/jq.js',
            'js/page.js',
            'js/autogrow.js',
            'js/textsaver.js',
        ),
        filters='jsmin',
        output='cache/packed.js')

#Scss
scss = Bundle(
       'scss/normalize.scss',
       'scss/foundation.scss',
        filters='scss',
        output='cache/scss.css'
)

#Css
register('all_css',
        Bundle(
               #scss,
               'css/app.css',
               'css/main.css',
        ),
        filters='cssmin',
        output='cache/packed.css')

