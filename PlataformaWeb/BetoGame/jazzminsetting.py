JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "BetoGame",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "BetoGame",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "BetoGame",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "/img/logo.png",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "/img/icono.ico",

    # Welcome text on the login screen
    "welcome_sign": "Bienvenido a BetoGame",

    # Copyright on the footer
    "copyright": "BetoGame",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "auth.User",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        # {"name": "Principal",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # # external url that opens in a new window (Permissions can be added)
        # # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # # model admin to link to (Permissions checked against model)
        # {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "Inventario"},
        {"app": "Local"},
        {"app": "Caja"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        # {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    # "order_with_respect_to": ["auth", "books", "books.author", "books.book"],
    "order_with_respect_to": ["auth"],

    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "Inventario": [{
    #         "name": "TestModel", 
    #         # "model": ["TestModel"],
    #         # "url": "make_messages", 
    #         "icon": "fa-solid fa-warehouse",
    #         # "permissions": ["books.view_book"]
    #     }]
    # },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "Inventario.Producto": "fas fa-hamburger",
        "Inventario.Entrada": "fas fa-truck-loading",
        "Inventario.HistoricoPrecios": "fas fa-dollar-sign",
        "Local.Cliente": "far fa-user-circle",
        "Local.Venta": "fas fa-shopping-cart",
        "Local.Juego": "fab fa-playstation",
        "Local.Consola": "fas fa-gamepad",
        "Local.Sesion": "fas fa-stopwatch",
        "Caja.Cuenta": "fas fa-cash-register",
        "Caja.Pago": "fas fa-file-invoice-dollar",
        "Caja.Cierre": "fas fa-book",
        "Caja.Variable": "fas fa-subscript",
        "Caja.HistoricoValores": "fas fa-search-dollar"
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "jazzmin/css/main.css",
    "custom_js": "jazzmin/js/main.js",
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

#######################################
# Currently available UI tweaks       #
# Use the UI builder to generate this #
#######################################

DEFAULT_UI_TWEAKS = {
    # Small text on the top navbar
    "navbar_small_text": False,
    # Small text on the footer
    "footer_small_text": True,
    # Small text everywhere
    "body_small_text": False,
    # Small text on the brand/logo
    "brand_small_text": False,
    # brand/logo background colour
    "brand_colour": False,
    # Link colour
    "accent": "accent-dark",
    # topmenu colour
    "navbar": "navbar-black navbar-dark",
    # topmenu border
    "no_navbar_border": False,
    # Make the top navbar sticky, keeping it in view as you scroll
    "navbar_fixed": True,
    # Whether to constrain the page to a box (leaving big margins at the side)
    "layout_boxed": False,
    # Make the footer sticky, keeping it in view all the time
    "footer_fixed": True,
    # Make the sidebar sticky, keeping it in view as you scroll
    "sidebar_fixed": True,
    # sidemenu colour
    "sidebar": "sidebar-dark-info",
    # sidemenu small text
    "sidebar_nav_small_text": False,
    # Disable expanding on hover of collapsed sidebar
    "sidebar_disable_expand": False,
    # Indent child menu items on sidebar
    "sidebar_nav_child_indent": False,
    # Use a compact sidebar
    "sidebar_nav_compact_style": False,
    # Use the AdminLTE2 style sidebar
    "sidebar_nav_legacy_style": True,
    # Use a flat style sidebar
    "sidebar_nav_flat_style": True,
    # Bootstrap theme to use (default, or from bootswatch, see THEMES below)
    # "theme": "flatly",
    # "theme": "yeti",
    "theme": "litera",
    # "theme": "minty",
    # "theme": "sandstone",
    # "theme": "simplex",
    # "theme": "spacelab",
    # "theme": "united",
    # Theme to use instead if the user has opted for dark mode (e.g darkly/cyborg/slate/solar/superhero)
    "dark_mode_theme": None,
    # The classes/styles to use with buttons
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}