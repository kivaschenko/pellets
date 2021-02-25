def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('search', '/search-results')
    # goods
    config.add_route('goods', '/table-goods')
    config.add_route('goods_detail', '/goods/{goods_id}')
    config.add_route('goods_action', '/goods/{action}',
        factory='pellets.security.GoodsFactory')
    # authentication
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signup', '/signup')
    # offers
    config.add_route('view_offer', '/offer/{offer_id}')
    config.add_route('map', '/map', factory='pellets.security.OfferFactory')
    config.add_route('offers', '/offers')
    config.add_route('offer_action', '/offer_action/{action}',
        factory='pellets:security.OfferFactory')
