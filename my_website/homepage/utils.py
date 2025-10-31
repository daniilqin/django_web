class HomeContextMixin:
    """
    Миксин для классов представлений приложения "homepage".

    Как использовать:
      - Наследовать миксин ПЕРВЫМ: class SomeView(HomeContextMixin, DetailView)
      - По необходимости задать атрибут `page_title` (строка или None).
      - В get_context_data вернуть объединённый контекст:
          return self.get_mixin_context(super().get_context_data(**kwargs), any_key=value)

    Миксин добавляет в контекст:
      - title (если задан атрибут `page_title`)
      - любые дополнительные пары ключ-значение, переданные в метод
        get_mixin_context(...)
    """

    page_title: str | None = None
    paginate_by = 3

    def get_mixin_context(self, context, **kwargs):
        if self.page_title:
            context['title'] = self.page_title
        if kwargs:
            context.update(kwargs)
        return context
