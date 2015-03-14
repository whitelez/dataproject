from django.conf.urls import patterns, url

from traffic import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^parking/$', views.parking, name='parking'),
    url(r'^camera/$', views.camera, name='camera'),
    url(r'^ajaxtest/$',views.ajaxtest, name='ajaxtest'),
    url(r'^parking_geoJSON/$', views.street_parking_geojson, name='parking_geoJSON' ),
    url(r'^parking_geoJSON_prediction/$', views.street_parking_geojson_prediction, name='parking_geoJSON_prediction' ),
    url(r'^count/$', views.count, name='count'),
    url(r'^weather/$', views.weather, name='weather'),
    url(r'^get_county_weather/$', views.get_county_weather, name = 'get_county_weather'),
    url(r'^get_weather/$', views.get_weather, name = 'get_weather'),
    url(r'^ev_stations/$', views.ev_stations, name='ev_stations'),
    url(r'^travel_time/$', views.travel_time, name='travel_time'),
#BY PXD
    url(r'^travel_time_new/$', views.travel_time_new, name='travel_time_new'),
    url(r'^get_node_info_for_one_corridor/$', views.get_node_info, name='get_node_info'),
    url(r'^get_spc_traveltime/$', views.get_spctraveltime, name='get_spctraveltime'),
    url(r'^get_spc_traveltimeformanyyears/$', views.get_spctraveltimeformanyyears, name='get_spctraveltimeformanyyears'),
    url(r'^get_spc_years/$', views.get_spcyears, name='get_spcyears'),
#END
    url(r'^get_travel_time/$', views.get_travel_time, name='get_travel_time'),
    url(r'^get_travel_time_prediction/$', views.get_travel_time_prediction, name='get_travel_time_prediction'),
    url(r'^get_road_tmc/$', views.get_road_tmc, name='get_road_tmc'),
    url(r'^incidents/$', views.incidents, name='incidents'),
    url(r'^get_incidents_rcrs/$', views.get_incidents_rcrs, name='get_incidents_rcrs'),
    url(r'^download/$', views.download, name='download'),
    url(r'^transit_data/$', views.transit_data, name='transit_data'),
    url(r'^transit/$', views.transit, name='transit'),
    url(r'^get_route/$', views.get_route, name='get_route'),
    url(r'^get_stops/$', views.get_stops, name='get_stops'),
    url(r'^transit_metrics/$',views.transit_metrics, name = 'transit_metrics'),
    url(r'^routing/$', views.routing, name='routing'),
    url(r'^routing_path/$', views.routing_path, name='routing_path'),
    url(r'^parking_lots/$', views.parking_lots, name='parking_lots'),
    url(r'^test/$', views.test, name='test'),
    url(r'^get_incidents_rcrs_area/$', views.get_incidents_rcrs_area, name='get_incidents_rcrs_area'),
    url(r'^real_time_incidents_rcrs/$', views.real_time_incidents_rcrs, name='real_time_incidents_rcrs'),
#SGYang
    url(r'^road_closure/$', views.closure, name='closure'),
)
