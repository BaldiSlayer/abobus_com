ymaps.ready(init);
    
var myMap, myPlacemark;

var coordinates1;

function a() {
    return coordinates1;    
}

function init() {
    // Создание карты.
    var myMap = new ymaps.Map("map", {
        // Координаты центра карты, Порядок по умолчанию: «широта, долгота».
        center: [55.76, 37.64],
        zoom: 9
    });
    
    function do_marker(s) {
        var searchArr = [s];
    
        searchArr.forEach(function(item) {
            ymaps.geocode(item, {
            results: 1
        }).then(function (res) {
                var firstGeoObject = res.geoObjects.get(0),
                    coords = firstGeoObject.geometry.getCoordinates();
                myMap.geoObjects.add(firstGeoObject);
    
                coordinates1 = coords;
            });
        }); 
    }
}