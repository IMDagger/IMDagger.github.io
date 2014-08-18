# -*- coding: utf-8 -*-
import bs4
import cgi
import six
from pelican import utils
from pelican import signals
from pelican import contents
from docutils import nodes, utils
from docutils.parsers.rst import Directive, directives, states
from docutils.parsers.rst.directives import images
from docutils.parsers.rst.roles import set_classes
from pygments.formatters import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
import pelican.settings as pys

class CutBlock(Directive):

    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'paragraph': lambda arg: directives.choice(arg, ('yes', 'no')),
    }
    final_argument_whitespace = True
    has_content = True

    def run(self):
        self.assert_has_content()
        container = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, container)

        ref_name = 'cut_{0}'.format(id(container))
        link = nodes.reference(refid=ref_name)
        link['data-attributes'] = {
            'toggle': 'collapse',
        }
        link['classes'] += ['h-link',]
        link += nodes.Text(self.arguments[0])

        if self.options.get('paragraph') == 'yes':
            cut_wrapper = nodes.paragraph()
        else:
            cut_wrapper = nodes.inline()
        cut_wrapper['classes'] += ['cut',]
        cut_wrapper += link

        container['classes'] += ['collapse',]
        container['ids'] += [ref_name,]
        return [cut_wrapper, container]

class PhotoBlock(images.Image):
    option_spec = images.Image.option_spec.copy()
    option_spec['title'] = option_spec['alt']
    option_spec['link'] = option_spec['target']
    del option_spec['alt'], option_spec['target']

    def run(self):
        self.options['target'] = self.options['link']
        self.options['alt'] = self.options['title']
        del self.options['title'], self.options['link']

        (image_node,) = images.Image.run(self)
        if isinstance(image_node, nodes.system_message):
            return [image_node,]
        p_block = nodes.paragraph(classes=['row', 'photo-item'])
        p_block += image_node
        return [p_block,]

def add_images_hint(sender):
    article = sender
    if article._content is None:
        return
    body = bs4.BeautifulSoup(article._content).body
    if not body:
        return
    for img in body.select('img'):
        if 'alt' in img.attrs:
            img['title'] = img['alt']

    if body.select('img'):
        article._content = u''.join(unicode(x) for x in body.children)

def underscored(sender, metadata):
    for key, value in metadata.items():
        if '-' in key:
            metadata[key.replace('-', '_')] = metadata[key]

def mood(sender):
    date = None
    last_mood = None
    for article in sender.articles:
        if article.category == 'mood' and (date is None or date < article.date):
            last_mood = article.content
            date = article.date
    if last_mood is not None:
        sender.mood = last_mood
        sender._update_context(('mood',))

def photo(sender):
    date = None
    last_photo = None
    for article in sender.articles:
        if article.category == 'photo' and (date is None or date < article.date) \
           and hasattr(article, 'tags') and u'Я' in article.tags:
            img = [line.split('::')[1] for line in open(article.source_path) if line.startswith('.. photo-block::')][0]
            sender.settings['ME']['PHOTO']['url'] = img
            sender.settings['ME']['PHOTO']['article'] = article
            date = article.date

class YaVideo(Directive):
    """ Embed Yandex Video video in posts.

    Based on the YouTube directive by Brian Hsu:
    https://gist.github.com/1422773

    VIDEO_ID is required, with / height are optional integer,
    and align could be left / center / right.

    Usage:
    .. yavideo:: VIDEO_ID
        :width: 640
        :height: 480
        :align: center
    """

    def align(argument):
        """Conversion function for the "align" option."""
        return directives.choice(argument, ('left', 'center', 'right'))

    required_arguments = 1
    optional_arguments = 2
    option_spec = {
        'width': directives.positive_int,
        'height': directives.positive_int,
        'align': align,
        'id': directives.unchanged,
    }

    final_argument_whitespace = False
    has_content = False

    def run(self):
        video_id = self.arguments[0].strip()
        width = 420
        height = 315
        align = 'left'

        if 'width' in self.options:
            width = self.options['width']

        if 'height' in self.options:
            height = self.options['height']

        if 'align' in self.options:
            align = self.options['align']

        safe_url = cgi.escape('http://flv.video.yandex.ru/lite/imdagger/{}/'.format(video_id), quote=True)
        div_block = '<div class="yavideo" align="{}">'.format(align)

        obj_id = self.options.get('id', 'flash')
        params = ''.join([
            '<param value="{}" name="movie">'.format(safe_url),
            '<param value="high" name="quality">',
            '<param value="transparent" name="wmode">',
            '<param value="#ffffff" name="bgcolor">',
            '<param value="true" name="allowfullscreen">',
            '<param value="sameDomain" name="allowscriptaccess">',
            '<param value="scale" name="scale">',
        ])
        embed_block = '<object id="{}" width="{}" height="{}" data="{}" '\
                      'type="application/x-shockwave-flash">{}</object>'.format(obj_id, width, height, safe_url, params)

        return [
            nodes.raw('', div_block, format='html'),
            nodes.raw('', embed_block, format='html'),
            nodes.raw('', '</div>', format='html'),
        ]

class SmartFormatter(HtmlFormatter):

    def _format_lines(self, tokensource):
        for t, value in HtmlFormatter._format_lines(self, tokensource):
            if t == 1:
                yield t, value.replace('$$strong$$', '<strong>').replace('$$/strong$$', '</strong>')
            else:
                yield t, value

class SmartCodeBlock(Directive):
    """ Source code syntax highlighting.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'anchorlinenos': directives.flag,
        'classprefix': directives.unchanged,
        'hl_lines': directives.unchanged,
        'lineanchors': directives.unchanged,
        'linenos': directives.unchanged,
        'linenospecial': directives.nonnegative_int,
        'linenostart': directives.nonnegative_int,
        'linenostep': directives.nonnegative_int,
        'lineseparator': directives.unchanged,
        'linespans': directives.unchanged,
        'nobackground': directives.flag,
        'nowrap': directives.flag,
        'tagsfile': directives.unchanged,
        'tagurlformat': directives.unchanged,
    }
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()

        # Fetch the defaults
        if pys.PYGMENTS_RST_OPTIONS is not None:
            for k, v in six.iteritems(pys.PYGMENTS_RST_OPTIONS):
                # Locally set options overrides the defaults
                if k not in self.options:
                    self.options[k] = v

        if ('linenos' in self.options and
                self.options['linenos'] not in ('table', 'inline')):
            if self.options['linenos'] == 'none':
                self.options.pop('linenos')
            else:
                self.options['linenos'] = 'table'

        for flag in ('nowrap', 'nobackground', 'anchorlinenos'):
            if flag in self.options:
                self.options[flag] = True

        # noclasses should already default to False, but just in case...
        formatter = SmartFormatter(noclasses=False, **self.options)
        parsed = highlight('\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

def register():
    signals.content_object_init.connect(add_images_hint)
    signals.article_generator_finalized.connect(mood)
    signals.article_generator_finalized.connect(photo)
    signals.article_generator_context.connect(underscored)
    directives.register_directive('photo-block', PhotoBlock)
    directives.register_directive('yavideo', YaVideo)
    directives.register_directive('cut', CutBlock)
    directives.register_directive('smart-code-block', SmartCodeBlock)