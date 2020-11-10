def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('search', '/search-results')
    # goods
    config.add_route('goods', '/table-goods')
    config.add_route('goods_detail', '/goods/{goods_id}')
    config.add_route('goods_action', '/goods/{action}')
    # authentication
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signup', '/signup')
    # offers
    config.add_route('view_offer', '/offer/{offer_id}')
    config.add_route('offers_at_map', '/map')
    config.add_route('offers', '/offers')
    config.add_route('create_offer', '/create_offer')
