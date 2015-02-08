Bumblebee обновление в 14.04 LTS
================================
:date: 2015-02-08 04:58
:tags: ubuntu, bumblebee, nvidia-prime, ion2
:category: link
:author: IMDagger
:attached-url: https://wiki.archlinux.org/index.php/bumblebee#.2Fdev.2Fdri.2Fcard0:_failed_to_set_DRM_interface_version_1.4:_Permission_denied

После обновления пакетов включился вдруг nvidia-prime, не
знаю в каком он сейчас состоянии (продукт от Nvidia), но
совсем недавно, чтобы переключить карточку, в нём нужно было
завершать текущий сеанс пользователя и входить снова, что
для меня не приемлимо. В Bumblebee никуда не нужно выходить,
всё переключается при помощи :code:`optirun` тут же по месту
в сеансе, при чём для каждого приложения можно выборочно.
После прописывания конкретного драйвера ядра в bumblebee.conf на
:code:`nvidia-331-updates` и переброса ссылки с nvidia-current на
nvidia-331-updates (была на nvidia-331-updates-prime), вылезла
вот такая ошибка:

 | /dev/dri/card0: failed to set DRM interface version 1.4: Permission denied

Решается добавкой описанной в вики:

 |  Section "Screen"
 |      Identifier "Default Screen"
 |      Device "DiscreteNvidia"
 |  EndSection
