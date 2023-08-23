var map, layer1, layer2wfs, layerJSON, layerBase1, layerBase2;
var controlZoomin,controlPan,controlSelect;


var style1 = new ol.style.Style({
	fill: new ol.style.Fill({
		color: [0, 255, 0, 1]
	}),
	stroke: new ol.style.Stroke({
		color: [0, 0, 0, 0.5],
		width: 1
	})
});

var style2 = new ol.style.Style({
	fill: new ol.style.Fill({
		color: [255, 0, 0, 1]
	}),
	stroke: new ol.style.Stroke({
		color: [0, 0, 0, 0.5],
		width: 1
	})
});

var style3 = new ol.style.Style({
	fill: new ol.style.Fill({
		color: [0, 0, 255, 1]
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


		layer1 = new ol.layer.Vector({
		   source: new ol.source.Vector({
                url: 'http://igeomedia.com:5556/map/',
                format: new ol.format.GeoJSON({
                })
            }),
		style:style1
        });
		
		layer2wfs = new ol.layer.Vector({
           source: new ol.source.Vector({
			    url:"http://http:/igeomedia.com:5556/map/?year=2000",
                format: new ol.format.GeoJSON({
                })
            }),
		style:style2
		});
		
		layerJSON = new ol.layer.Vector({
			source: new ol.source.Vector({
				url:'http://igeomedia.com:5556/map/?name=Armand-Duplessis',
				format: new ol.format.GeoJSON({
				})
            }),
		style:style3
		});

		layer2wfs.setVisible(false);
		layerJSON.setVisible(false);

		layerBase1 = new ol.layer.Tile({source: new ol.source.OSM()});

		
		//layerBase2 = ...
		
		layerBase1.setVisible(true);
		//layerBase2.setVisible(false);
		
		
		map = new ol.Map({
          
        target: 'map',
        
        view: new ol.View({
          projection: 'EPSG:3857',
          center: ol.proj.transform([-71.8934,45.4106],'EPSG:4326','EPSG:3857'),
          zoom: 14
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
