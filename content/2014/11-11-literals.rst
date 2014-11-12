syntax-parse и литералы
=======================

:date: 2014-11-11 04:15
:tags: racket, literals, syntax-parse, биндинг, связывание, синтаксис
:category: text
:author: IMDagger

При использовании :code:`syntax-parse` все литералы из :code:`\#\:literals`
должны быть обязательно объявлены, в отличие от syntax-case, в котором
литералы это нечто ближе к данным, а не к синтаксическим переменным.

.. code-block:: cl

   (define-syntax (:pre stx) (raise-syntax-error stx 'pre "Cannot be used outside syntax ..."))
   (define-syntax (test stx)
     (syntax-parse #:literals (:pre)
       [ ... ]))

Если так не сделать, то Racket будет ругаться, что :code:`syntax-parse\: literal is unbound in phase 0 (phase 0 relative to the enclosing module)`\ .
