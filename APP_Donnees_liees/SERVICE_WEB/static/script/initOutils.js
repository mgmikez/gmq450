

function creationBarreOutils(){

				$("#toolbar").controlgroup();
				
				$("#extent").click(function(){
					map.setView(
						new ol.View({
							projection: 'EPSG:3857',
							center: ol.proj.transform([-89,44],'EPSG:4326','EPSG:3857'),
							zoom: 6
						})
					)
					controlZoomin.setActive(false);
					controlPan.setActive(true);
					controlSelect.setActive(false);
					$("#infoPanel").text("Cliquer sur l'element a interroger");
					$( "#accordion" ).accordion( "option", "active", 0 );
				});
				
				$("#zoomin").click(function(){
					controlZoomin.setActive(true);
					controlPan.setActive(false);
					controlSelect.setActive(false);
					$("#infoPanel").text("Cliquer sur l'element a interroger");
					$( "#accordion" ).accordion( "option", "active", 0 );
				});
				
				$("#pan").click(function(){
					controlZoomin.setActive(false);
					controlPan.setActive(true);
					controlSelect.setActive(false);
					$("#infoPanel").text("Cliquer sur l'element a interroger");
					$( "#accordion" ).accordion( "option", "active", 0 );
				});
				
				$("#info").click(function(){
						$( "#accordion" ).accordion( "option", "active", 1 );
						controlSelect.setActive(true);
					} );

}