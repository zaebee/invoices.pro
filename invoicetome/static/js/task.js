var app = app || {};

(function (app) {
  app.tasks = new Ractive({
    el: '#task-list',
    template: '#task-template',
    data: {
      tasks: new app.Tasks(), // наша Backbone модель

      // хэлпер используется в шаблоне {{ format(price) }}
      format: function ( num ) {
        return parseFloat(num).toFixed( 2 );
      },

      // хэлпер используется в шаблоне {{ total_tasks(tasks) }}
      total_tasks: function ( collection ) {
        var total = collection.reduce(function( sum, el ) {
          var total = el.get('quantity') * el.get('unit_price');
          el.set('total', parseFloat(total));
          return el.get('quantity') * el.get('unit_price') + sum;
        }, 0 );
        return total.toFixed( 2 );
      },
    },
    adaptors: [ Ractive.adaptors.Backbone ],
  });

  app.tasks.on({

    // Обрабатываем нажатие на кнопку создания таска
    // в шаблоне `on-click="add"`
    add: function ( event ) {
      if (event && event.first) {
        var params =  {
          description: gettext('Supporting of in-house project (hours worked)'),
          quantity: 40,
          unit_price: 125,
          total: 6000,
        }
      } else {
        var params = {
          description: '',
          quantity: 0,
          unit_price: 0,
          total: 0,
        };
      };
      var tasks = this.get('tasks');
      var task = new app.Task(params);
      tasks.add(task);
      /*
      task.save(null, {
        // хак, чтобы привязать новый созданный таск к текущему инвойсу
        success: function() {
          task.set('invoice', app.invoice.data.invoice.id);
          task.save();
        }
      });
      */
    },

    save: function ( event ) {
      this.get('tasks').each(function ( task ) {
        task.save();
      });
    },

    // удаляем таск с сервера тоже
    destroy: function ( event ) {
      var task = this.get('tasks').last();
      if (task) {
        task.destroy();
      };
    },

  });

  // подписываемся на изменения параметров `hours` и `rate` для тасков
  // чтобы пересчитивать сумму
  // сумму также меняем у инвойса
  // TODO нужно сохранять инвойс после изменения суммы
  app.tasks.observe('tasks.*.quantity tasks.*.unit_price', function(tasks, old, keypath){
    var subtotal = this.data.total_tasks(this.data.tasks);
    app.invoice.set('invoice.subtotal', parseFloat(subtotal));
  });
  // Добавляем первый заполненный таск и 7 пустых
  app.tasks.fire('add', {first: true});
  _.each(_.range(7), function(el){
    app.tasks.fire('add');
  });

})(app);
