{
    'name' : "Arkana Module",
    'depends' : [
        'base',
        ],
    'data' : [
        'views/arkana_property_views.xml',
        'views/arkana_property_type_views.xml',
        'views/arkana_property_tag_views.xml',
        'views/arkana_property_offer_views.xml',
        'views/arkana_menus.xml',
        'security/ir.model.access.csv',
        ],

    'application' : True,
    'installable' : True,
}