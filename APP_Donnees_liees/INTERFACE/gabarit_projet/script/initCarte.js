var map, layer1, layer2wfs, layerJSON, layerBase1, layerBase2;
var controlZoomin,controlPan,controlSelect;


var PNQStyle = new ol.style.Style({
	fill: new ol.style.Fill({
		color: [0, 255, 0, 1]
	}),
	stroke: new ol.style.Stroke({
		color: [0, 0, 0, 0.5],
		width: 1
	})
});

function creationCarte(){
	
		controlZoomin = new ol.interaction.DragZoom();
		controlPan = new ol.interaction.DragPan();
		controlSelect = new ol.interaction.Select();
		controlSelect.setActive(false);


		layer1 = new ol.layer.Tile({source: new ol.source.TileWMS({
                url: 'https://igeomedia.com/cgi-bin/mapserv?map=/home/mickael/mapfile/tutoriel3.map&',
                params: {LAYERS: 'urbanLayer', VERSION: '1.1.1'}
            })
        });
		
		layer2wfs = new ol.layer.Vector({
           source: new ol.source.Vector({
			    url:"https://igeomedia.com/cgi-bin/mapserv?map=/home/mickael/mapfile/tutoriel3.map&service=wfs&version=1.1.0&request=getfeature&typename=urbanLayer&srsName=EPSG:3857",
                format: new ol.format.WFS({
                })
            })  
		});
		
		layerJSON = new ol.layer.Vector({
			source: new ol.source.Vector({
				url:'./test_serviceWeb.geojson',
				format: new ol.format.GeoJSON({
				})
            }),
		style:PNQStyle 
		});

		layer2wfs.setVisible(false);

		layerBase1 = new ol.layer.Tile({source: new ol.source.OSM()});
		
		//layerBase2 = ...
		
		layerBase1.setVisible(true);
		//layerBase2.setVisible(false);
		
		
		map = new ol.Map({
          
        target: 'map',
        
        view: new ol.View({
          projection: 'EPSG:3857',
          center: ol.proj.transform([-71.852,45.399],'EPSG:4326','EPSG:3857'),
          zoom: 15
        }),
        
        layers: [layerBase1, layer1, layer2wfs, layerJSON],
        
        controls: ol.control.defaults().extend([
            new ol.control.ScaleLine(),
            new ol.control.MousePosition({
				coordinateFormat: ol.coordinate.createStringXY(4),
				projection: 'EPSG:4326',
				className: 'custom-mouse-position',
				target: document.getElementById('mouse-position'),
			}),
            new ol.control.FullScreen()
          ]),
		  
		interactions: ol.interaction.defaults({
			dragPan: false,
			dragZoom: false
		}).extend([
			controlZoomin,controlPan,controlSelect
		]), 
          
      });
	  
	  controlSelect.on('select', function(evt){
		var selected = evt.selected;

		selected.forEach(function(feature){
            		$("#infoPanel").text(feature.getProperties().name +" "+feature.getProperties().state);
        });
    
    });



}
