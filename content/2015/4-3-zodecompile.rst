raco decompile
==========================================
:date: 2015-04-03 03:39
:tags: racket, raco, decompile, zo
:category: text
:author: IMDagger

Интересно сделано получение встроенной функции по номеру в :code:`compiler/decompile`.
Ведь встроенные константы в Racket помещаются в специальные глобальные ячейки и имеют
свои номера. Соответственно в zo-байткод попадают только числа. И в языке доступна только проверка
при помощи :code:`primitive?` и ещё пару методов связанных с примитивами. Также есть
возможность получить текущие объявления из :code:`(namespace-mapped-symbols)`.

Так вот :code:`decompile` делает хитрый трюк, не применяя никаких хаков: создаёт пустой
namespace, делает :code:`require` всяких встроенных модулей в пространство (типа :code:`'#%kernel`
:code:`'#%unsafe` :code:`'#%flfxnum` :code:`'#%extfl` :code:`'#%futures` :code:`'#%foreign`), затем
пробегается по списку объявленных констант и вызывает для каждой из них
стандартный :code:`compile`. Если константа скомпилировалась, то пробует её распарсить при помощи
:code:`zo-parse`. Ну а дальше, просто выполняет :code:`match` по выражению и, вуаля, получает число из
структуры primval:

.. code-block:: racket

   ...
   (let ([n (match v
                [(struct compilation-top (_ prefix (struct primval (n)))) n]
                [else #f])])
          (hash-set! table n (car b)))
   ...
