var map, layerBase1, layerBase2, layerBase3, parcLayer, linkedLayer;
var controlZoomin,controlPan,controlSelect;

function creationCarte(){
	
	controlZoomin = new ol.interaction.DragZoom();
	controlPan = new ol.interaction.DragPan();
	controlSelect = new ol.interaction.Select();
	controlSelect.setActive(true);

	layerBase1 = new ol.layer.Tile({source: new ol.source.OSM()});
		
	layerBase2 = new ol.layer.Tile({source: new ol.source.Stamen({layer: 'terrain'}) });

	layerBase3 = new ol.layer.Tile({source: new ol.source.XYZ({
		url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
		maxZoom: 19
		}) 
	});

	// Créez une nouvelle couche vecteur pour le geojson des parcs
	var parcLayer = new ol.layer.Vector({
		source: new ol.source.Vector({
		url: 'static/data/parc.geojson', 
		format: new ol.format.GeoJSON(),
		style: new ol.style.Style({
			fill: new ol.style.Fill({
				color: 'rgba(255, 255, 255, 0.8)' // Red fill color with 50% opacity
			  }),
			  stroke: new ol.style.Stroke({
				color: 'rgba(255, 0, 0, 1)', // Red stroke color
				width: 2 // Stroke width in pixels
			  })
			})
		})
	});

	// Créez une nouvelle couche vecteur pour le geojson des parcs
	var linkedLayer = new ol.layer.Vector({
		source: new ol.source.Vector({
		url: 'http://igeomedia.com:5556/map', 
		format: new ol.format.GeoJSON(),
		style: new ol.style.Style({
			fill: new ol.style.Fill({
				color: 'rgba(255, 255, 0, 0.5)' // Red fill color with 50% opacity
				}),
				stroke: new ol.style.Stroke({
				color: 'rgba(255, 0, 0, 1)', // Red stroke color
				width: 2 // Stroke width in pixels
				})
			})
		})
	});

	layerBase1.setVisible(false);
	layerBase2.setVisible(false);
	layerBase3.setVisible(true);
	parcLayer.setVisible(true);
	linkedLayer.setVisible(true);

	map = new ol.Map({
		target: 'map',
		view: new ol.View({
			projection: 'EPSG:3857',
			center: ol.proj.transform([-71.8880,45.4240],'EPSG:4326','EPSG:3857'),
			zoom: 17}),
		layers: [layerBase1, layerBase2, layerBase3, parcLayer, linkedLayer],
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

	// Attacher un événement de clic à l'interaction Select
	controlSelect.on('select', function (event) {
		/* Réinitialiser le contenu de content1, content2 et content3 */
		var content1 = document.getElementById("content1");
		var content2 = document.getElementById("content2");
		var content3 = document.getElementById("content3");
		content1.innerHTML = "";
		content2.innerHTML = "";
		content3.innerHTML = "";
		/* Récupération des infos à partir des polygones */
		var selectedFeatures = controlSelect.getFeatures();
		var selectedPolygon = selectedFeatures.item(0); 
		if (selectedPolygon) {
			/* Changement du titre */
			var parc_name = "Parc Caron" //selectedPolygon.getProperties().name;
			var parcname = document.getElementById("parcname");
			parcname.innerHTML = parc_name;
			/* Tout ce qui est ici va être à modifier avec les infos provenant des requetes */
			var topo_name = "Richard Caron";
			var topo_DOB = "13 septembre 1947";
			var topo_profession = "Bénévole";
			var topo_image = ["static/images/topo_caron.jpg"];
			var parc_image = ["static/images/parc_caron.jpg"];
			var parc_area = "0.3 ha" //selectedPolygon.getProperties().init_area;
			var parc_type = "Parc de voisinage";
			var parc_arr = "Fleurimont";
			var parc_DOC = "Entre 1963 et 1965";
			var parc_oldName = "parc Apollo";
			//var parc_currentNameDate = selectedPolygon.getProperties().currentnamedate;
			var parc_utilities = "Balançoire, bancs, arbres"
			/* ---------------------------------------------------------------------------- */
			/* Menu TOPO */
			var image = document.createElement("img");
			image.src = topo_image;
			image.id = "topo_image";
			var toponame = document.createElement("div");
			toponame.innerHTML = "<u>Nom</u>" + " : " + topo_name;
			var topoDOB = document.createElement("div");
			topoDOB.innerHTML = "<u>Date de naissance</u>" + " : " + topo_DOB;
			var topoProfession = document.createElement("div");
			topoProfession.innerHTML = "<u>Profession</u>" + " : " + topo_profession;
			
			content1.appendChild(image);
			content1.appendChild(toponame);
			content1.appendChild(topoDOB);
			content1.appendChild(topoProfession);

			/* Menu PARC */
			var image = document.createElement("img");
			image.src = parc_image;
			image.id = "parc_image";
			var parcArea = document.createElement("div");
			parcArea.innerHTML = "<u>Superficie</u>" + " : " + parc_area;
			var parcType = document.createElement("div");
			parcType.innerHTML = "<u>Type</u>" + " : " + parc_type;
			var parcArr = document.createElement("div");
			parcArr.innerHTML = "<u>Arrondissement</u>" + " : " + parc_arr;
			var parcDOC = document.createElement("div");
			parcDOC.innerHTML = "<u>Date de création</u>" + " : " + parc_DOC;
			//var currentNameDate = document.createElement("div");
			//currentNameDate.innerHTML = "<u>Nom actuel depuis</u>" + " : " + parc_currentNameDate;
			var parcOldName = document.createElement("div");
			parcOldName.innerHTML = "<u>Ancien nom</u>" + " : " + parc_oldName;	
			var parcUtilities = document.createElement("div");
			parcUtilities.innerHTML = "<u>Aménagements</u>" + " : " + parc_utilities;

			content2.appendChild(image);
			content2.appendChild(parcArea);
			content2.appendChild(parcType);
			content2.appendChild(parcArr);
			content2.appendChild(parcDOC);
			//content2.appendChild(currentNameDate);
			content2.appendChild(parcOldName);
			content2.appendChild(parcUtilities);

			/*Menu AUTRE */
			var docLink = document.createElement("a");
			docLink.href = "https://igeomedia.com/~gev/Caron.pdf";
			docLink.innerHTML = "<u>Lien vers la fiche descriptive du parc</u>"; // Le texte du lien, souligné
			content3.appendChild(docLink);
		}
	});

	map.on('click', function (event) {
		content1.innerHTML = "";
	});

}

/*http://igeomedia.com:5556/map/?name=Armand-Duplessis*/