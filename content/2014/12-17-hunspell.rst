Emacs и Hunspell
=======================

:date: 2014-12-17 14:27
:tags: emacs, spellcheck, hunspell, aspell, проверка, UTF-8
:category: text
:author: IMDagger

Раньше у меня с Emacs использовалась проверка через Aspell,
но так можно проверять только один язык в тексте, либо собирать
мультиязыковой словарь. Я решил посмотреть, может ли Hunspell
просто принять в качестве аргументов несколько словарей, и да,
он может это. Поэтому я сделал выбор в пользу него.
Хотя на этом пути тоже возникли свои подводные камни связанные
с тем, что в пакетах старая сборка Hunspell. А в ней есть
`ошибка <http://debbugs.gnu.org/cgi/bugreport.cgi?bug=7781>`__ при
работе с UTF-8, когда утилита выводит номер
байта вместо номера символа. Поэтому пришлось собрать
пакет из `исходников <http://sourceforge.net/projects/hunspell/>`__\.
А ещё установить пакет  hunspell-ru-ie-yo из
`ppa:andrew-crew-kuznetsov/xneur-stable <https://launchpad.net/~andrew-crew-kuznetsov/+archive/ubuntu/xneur-stable>`__
от команды XNeur, чтобы была в словарях бука **Ё**.

Устанавливаем пакет Hunspell и языки.

.. code-block:: sh

   $ ./configure.sh --prefix=/usr
   $ sudo checkinstall make # используем утилиту для сборки deb
   ...
   $ sudo apt-get install hunspell-en-us hunspell-ru-ie-yo

Правда последняя версии чекера из SVN немного медленная и пришлось
нарастить timeout-ы в :code:`flyspell-lazy.el`. Включить другой движок для
Emacs не составляет большой проблемы.

.. code-block:: cl

   (custom-set-variables
    '(ispell-local-dictionary-alist
      '(("russian-english"
        "[АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюяA-Za-z]"
        "[^АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюяA-Za-z]"
        "[-']"  nil ("-d" "ru_RU,en_US") nil utf-8)))
    '(ispell-program-name "hunspell")
    '(ispell-dictionary "russian-english")
    '(ispell-really-aspell nil)
    '(ispell-really-hunspell t)
    '(ispell-encoding8-command t)
    '(ispell-silently-savep t)
    '(flyspell-delay 1))

В данном случае словарь russian-english это ключ, по которому происходит
поиск настроек. Где я уже указал опции :code:`-d ru_RU,en_US` и кодировку
ввода **UTF-8**.

..  LocalWords: Hunspell checkinstall
